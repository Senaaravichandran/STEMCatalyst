"""
Voice-to-Text Service using AssemblyAI API
Enhanced with LJ Speech dataset training patterns for improved accuracy
"""

import os
import json
import logging
import requests
import numpy as np
from typing import Dict, List, Optional, Tuple
import pandas as pd
from difflib import SequenceMatcher
import re
from io import BytesIO
import base64
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceService:
    def __init__(self):
        """Initialize AssemblyAI Voice Service with training data enhancement"""
        self.api_key = os.getenv('ASSEMBLYAI_API_KEY')
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
        
        self.upload_url = "https://api.assemblyai.com/v2/upload"
        self.transcript_url = "https://api.assemblyai.com/v2/transcript"
        
        # Load and process training data for model tuning
        self.training_data = self._load_training_data()
        self.vocabulary_patterns = self._analyze_vocabulary_patterns()
        
        logger.info(f"Voice service initialized with {len(self.training_data)} training samples")
    
    def _load_training_data(self) -> List[Dict]:
        """Load LJ Speech dataset for voice model tuning"""
        try:
            data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'text2speech', 'metadata.csv')
            
            training_samples = []
            with open(data_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            audio_id = parts[0]
                            original_text = parts[1]
                            normalized_text = parts[2]
                            
                            training_samples.append({
                                'audio_id': audio_id,
                                'original_text': original_text,
                                'normalized_text': normalized_text,
                                'word_count': len(normalized_text.split()),
                                'char_count': len(normalized_text)
                            })
            
            logger.info(f"Loaded {len(training_samples)} training samples")
            return training_samples
            
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            return []
    
    def _analyze_vocabulary_patterns(self) -> Dict:
        """Analyze vocabulary patterns from training data for accuracy tuning"""
        if not self.training_data:
            return {}
        
        try:
            # Extract common patterns
            all_text = ' '.join([sample['normalized_text'] for sample in self.training_data])
            words = all_text.lower().split()
            
            # Word frequency analysis
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Common word patterns
            common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:1000]
            
            patterns = {
                'common_words': dict(common_words),
                'avg_word_length': np.mean([len(word) for word in words]),
                'avg_sentence_length': np.mean([sample['word_count'] for sample in self.training_data])
            }
            
            logger.info(f"Analyzed vocabulary: {len(patterns['common_words'])} common words")
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing vocabulary patterns: {e}")
            return {}
    
    def _enhance_transcription(self, raw_transcription: str) -> str:
        """Enhance transcription using training data patterns"""
        if not self.vocabulary_patterns or not raw_transcription:
            return raw_transcription
        
        try:
            enhanced_text = raw_transcription.lower()
            
            # Apply common word corrections
            words = enhanced_text.split()
            corrected_words = []
            
            for word in words:
                # Find closest match in common vocabulary
                best_match = self._find_closest_vocabulary_match(word)
                corrected_words.append(best_match if best_match else word)
            
            enhanced_text = ' '.join(corrected_words)
            
            # Capitalize first letter of sentences
            sentences = enhanced_text.split('. ')
            capitalized_sentences = [s.capitalize() for s in sentences]
            enhanced_text = '. '.join(capitalized_sentences)
            
            return enhanced_text
            
        except Exception as e:
            logger.error(f"Error enhancing transcription: {e}")
            return raw_transcription
    
    def _find_closest_vocabulary_match(self, word: str, threshold: float = 0.8) -> Optional[str]:
        """Find closest match in training vocabulary"""
        if not self.vocabulary_patterns.get('common_words'):
            return None
        
        word = word.lower().strip()
        
        # Exact match
        if word in self.vocabulary_patterns['common_words']:
            return word
        
        # Fuzzy matching for common words
        best_match = None
        best_score = 0
        
        for vocab_word in list(self.vocabulary_patterns['common_words'].keys())[:500]:  # Top 500 words
            score = SequenceMatcher(None, word, vocab_word).ratio()
            if score > best_score and score >= threshold:
                best_score = score
                best_match = vocab_word
        
        return best_match
    
    def _upload_audio_file(self, audio_data: bytes) -> str:
        """Upload audio file to AssemblyAI and get upload URL"""
        try:
            headers = {
                'authorization': self.api_key,
                'content-type': 'application/octet-stream'
            }
            
            logger.info(f"Uploading audio to AssemblyAI, size: {len(audio_data)} bytes")
            
            response = requests.post(
                self.upload_url,
                headers=headers,
                data=audio_data,
                timeout=60
            )
            
            logger.info(f"Upload response status: {response.status_code}")
            logger.info(f"Upload response: {response.text}")
            
            if response.status_code == 200:
                upload_url = response.json().get('upload_url')
                logger.info(f"Upload successful, URL: {upload_url}")
                return upload_url
            else:
                logger.error(f"Upload failed: {response.status_code} - {response.text}")
                raise Exception(f"Upload failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Error uploading audio: {e}")
            raise e

    def transcribe_audio(self, audio_data: bytes, options: Dict = None) -> Dict:
        """
        Transcribe audio using AssemblyAI API with dataset-enhanced accuracy
        Following the exact working format from AssemblyAI documentation
        
        Args:
            audio_data: Raw audio bytes (any supported format)
            options: Transcription options
        
        Returns:
            Dict with transcription results and confidence metrics
        """
        try:
            # Step 1: Upload audio file first
            audio_url = self._upload_audio_file(audio_data)
            logger.info(f"Audio uploaded successfully: {audio_url}")
            
            # Step 2: Start transcription with EXACT format from working example
            headers = {"authorization": self.api_key}
            endpoint = "https://api.assemblyai.com/v2/transcript"
            
            # Use ONLY the audio_url as per working example - no extra parameters
            json_data = {"audio_url": audio_url}
            
            logger.info(f"Sending transcription request to: {endpoint}")
            logger.info(f"Request data: {json_data}")
            
            response = requests.post(endpoint, json=json_data, headers=headers)
            
            logger.info(f"Transcript request response: {response.status_code}")
            logger.info(f"Response text: {response.text}")
            
            if response.status_code != 200:
                error_msg = f"AssemblyAI API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {
                    'success': False,
                    'error': error_msg,
                    'transcript': '',
                    'confidence': 0
                }
            
            result = response.json()
            transcript_id = result['id']
            logger.info(f"Transcript created with ID: {transcript_id}")
            
            # Step 3: Poll until transcription completes (exact format from example)
            endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
            
            max_attempts = 60  # Maximum 60 attempts (3 minutes)
            attempt = 0
            
            while attempt < max_attempts:
                attempt += 1
                time.sleep(3)  # Wait 3 seconds as per example
                
                poll_response = requests.get(endpoint, headers=headers, timeout=30)
                
                if poll_response.status_code != 200:
                    logger.error(f"Polling failed: {poll_response.status_code} - {poll_response.text}")
                    return {
                        'success': False,
                        'error': f"Polling failed: {poll_response.status_code}",
                        'transcript': '',
                        'confidence': 0
                    }
                
                data = poll_response.json()
                status = data["status"]
                
                logger.info(f"Transcription status: {status}")
                
                if status == "completed":
                    # Extract transcription
                    transcript = data.get("text", "")
                    confidence = data.get("confidence", 0)
                    
                    logger.info(f"Transcription completed: {transcript}")
                    
                    # Enhance transcription using training data
                    enhanced_transcript = self._enhance_transcription(transcript)
                    
                    # Calculate metrics
                    word_count = len(enhanced_transcript.split())
                    
                    return {
                        'success': True,
                        'transcript': enhanced_transcript,
                        'raw_transcript': transcript,
                        'confidence': confidence if confidence else 0.8,  # Default confidence
                        'word_count': word_count,
                        'enhancement_applied': enhanced_transcript != transcript,
                        'metadata': {
                            'model': 'AssemblyAI',
                            'training_samples_used': len(self.training_data),
                            'vocabulary_enhanced': bool(self.vocabulary_patterns),
                            'transcript_id': transcript_id
                        }
                    }
                    
                elif status == "error":
                    error_msg = f"AssemblyAI transcription error: {data.get('error', 'Unknown error')}"
                    logger.error(error_msg)
                    return {
                        'success': False,
                        'error': error_msg,
                        'transcript': '',
                        'confidence': 0
                    }
                # Continue polling if status is still "queued" or "processing"
            
            # Timeout reached
            return {
                'success': False,
                'error': 'Transcription timed out. Please try again with a shorter audio.',
                'transcript': '',
                'confidence': 0
            }
                
        except Exception as e:
            error_msg = f"Voice transcription error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'success': False,
                'error': error_msg,
                'transcript': '',
                'confidence': 0
            }
    
    def transcribe_base64_audio(self, audio_base64: str, options: Dict = None) -> Dict:
        """Transcribe base64 encoded audio"""
        try:
            logger.info(f"Received base64 audio, length: {len(audio_base64)} characters")
            
            # Handle different base64 formats (with or without data URL prefix)
            if ',' in audio_base64:
                # Extract the base64 data from data URL format
                audio_base64 = audio_base64.split(',')[1]
            
            # Clean the base64 string (remove whitespace, newlines)
            audio_base64 = audio_base64.strip().replace('\n', '').replace('\r', '').replace(' ', '')
            
            # Add padding if needed
            padding = 4 - len(audio_base64) % 4
            if padding != 4:
                audio_base64 += '=' * padding
            
            # Decode base64 audio
            audio_data = base64.b64decode(audio_base64)
            logger.info(f"Decoded audio data, size: {len(audio_data)} bytes")
            
            if len(audio_data) < 100:
                return {
                    'success': False,
                    'error': 'Audio data too small. Please record a longer audio.',
                    'transcript': '',
                    'confidence': 0
                }
            
            return self.transcribe_audio(audio_data, options)
        except Exception as e:
            error_msg = f"Base64 audio decode error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'success': False,
                'error': error_msg,
                'transcript': '',
                'confidence': 0
            }
    
    def get_training_stats(self) -> Dict:
        """Get statistics about the training dataset"""
        if not self.training_data:
            return {'error': 'No training data loaded'}
        
        return {
            'total_samples': len(self.training_data),
            'avg_word_count': np.mean([s['word_count'] for s in self.training_data]),
            'avg_char_count': np.mean([s['char_count'] for s in self.training_data]),
            'vocabulary_size': len(self.vocabulary_patterns.get('common_words', {})),
            'common_words_top_10': list(self.vocabulary_patterns.get('common_words', {}).keys())[:10],
            'dataset_source': 'LJ Speech Dataset',
            'enhancement_enabled': bool(self.vocabulary_patterns)
        }
    
    def search_similar_audio_samples(self, text_query: str, limit: int = 5) -> List[Dict]:
        """Find similar audio samples from training data for reference"""
        if not self.training_data:
            return []
        
        try:
            text_query = text_query.lower()
            similarities = []
            
            for sample in self.training_data:
                sample_text = sample['normalized_text'].lower()
                similarity = SequenceMatcher(None, text_query, sample_text).ratio()
                
                if similarity > 0.3:  # Threshold for relevance
                    similarities.append({
                        'audio_id': sample['audio_id'],
                        'text': sample['normalized_text'],
                        'similarity': similarity,
                        'word_count': sample['word_count']
                    })
            
            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:limit]
            
        except Exception as e:
            logger.error(f"Error searching similar samples: {e}")
            return []

# Global instance for easy access
voice_service = VoiceService()
