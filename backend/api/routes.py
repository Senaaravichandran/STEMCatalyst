from flask import Blueprint, request, jsonify, current_app
import logging
from datetime import datetime
from typing import Dict, Any
from services.fallback_service import FallbackService

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

@api_bp.route('/solve', methods=['POST'])
def solve_problem():
    """
    Solve a STEM problem using multiple AI models with comprehensive error handling
    
    Expected JSON payload:
    {
        "problem": "problem statement",
        "subject": "Physics|Chemistry|Mathematics|Biology|Computer Science",
        "difficulty": "Beginner|Intermediate|Advanced|University|Graduate",
        "showSteps": true|false,
        "includeTheory": true|false,
        "includeDiagrams": true|false,
        "temperature": 0.2,
        "model": "llama|nemotron" (optional, defaults to llama)
    }
    """
    try:
        logger.info("Request: POST /api/solve")
        data = request.get_json()
        logger.info(f"Request data: {data}")
        
        # Validate required fields
        if not data or 'problem' not in data:
            error_msg = 'Problem statement is required'
            logger.error(f"Validation error: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        problem = data['problem'].strip()
        if not problem:
            error_msg = 'Problem statement cannot be empty'
            logger.error(f"Validation error: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        # Extract parameters with defaults
        subject = data.get('subject', 'Mathematics')
        difficulty = data.get('difficulty', 'Intermediate')
        show_steps = data.get('showSteps', True)
        include_theory = data.get('includeTheory', True)
        include_diagrams = data.get('includeDiagrams', True)
        temperature = data.get('temperature', 0.2)
        preferred_model = data.get('model', 'llama')
        
        logger.info(f"Processing {difficulty} {subject} problem")
        
        # Validate temperature
        if not isinstance(temperature, (int, float)) or temperature < 0 or temperature > 1:
            temperature = 0.2
            logger.warning(f"Invalid temperature provided, using default: {temperature}")
        
        # Get enhanced context from data service
        try:
            context = current_app.data_service.get_context_for_problem(problem, subject)
            logger.info("Context retrieved successfully from data service")
        except Exception as e:
            logger.warning(f"Failed to get context from data service: {str(e)}")
            context = None
        
        # Enhance problem with context if available
        enhanced_problem = problem
        if context:
            enhanced_problem = f"{problem}\n\nContext for reference:\n{context}"
            enhanced_problem = f"{problem}\n\nContext: {context}"
            logger.info("Enhanced problem with context data")
        
        # Call AI service with enhanced error handling and model selection
        try:
            logger.info(f"Calling AI service to solve problem using {preferred_model}")
            solution = current_app.ai_service.solve_problem(
                problem=enhanced_problem,
                subject=subject,
                difficulty=difficulty,
                show_steps=show_steps,
                include_theory=include_theory,
                include_diagrams=include_diagrams,
                temperature=temperature,
                preferred_model=preferred_model
            )
            logger.info(f"Problem solved successfully using {solution.get('model_used', 'AI')} service")
            
        except Exception as ai_error:
            logger.warning(f"AI service error: {str(ai_error)}")
            
            # Check if it's a rate limiting error
            if "429" in str(ai_error) or "Service tier capacity exceeded" in str(ai_error) or "rate" in str(ai_error).lower():
                logger.info(f"Rate limit detected, using fallback service for problem solving")
                
                # Use fallback service
                fallback_result = FallbackService.get_sample_solution(problem, subject, difficulty)
                
                return jsonify({
                    'success': True,
                    'solution': fallback_result['solution'],
                    'metadata': fallback_result['metadata']
                })
            
            # Provide user-friendly error messages based on error type
            error_message = str(ai_error)
            status_code = 500
            
            if "Network connection issue" in error_message or "getaddrinfo failed" in error_message:
                status_code = 503
                error_message = "Unable to connect to AI service. Please check your internet connection and try again."
            elif "Authentication issue" in error_message or "invalid" in error_message.lower():
                status_code = 401
                error_message = "AI service authentication failed. Please contact support."
            elif "Request timeout" in error_message or "timeout" in error_message.lower():
                status_code = 504
                error_message = "The AI service is taking too long to respond. Please try again."
            elif "Rate limit exceeded" in error_message or "rate limit" in error_message.lower():
                status_code = 429
                error_message = "Too many requests. Please wait a moment and try again."
            elif "All AI models are currently unavailable" in error_message:
                status_code = 503
                error_message = "All AI services are temporarily unavailable. Please try again later."
            
            return jsonify({
                'success': False,
                'error': error_message,
                'error_type': 'ai_service_error',
                'details': str(ai_error) if current_app.debug else None
            }), status_code
        
        # Log the successful request
        logger.info(f"Problem solved successfully - Subject: {subject}, Difficulty: {difficulty}")
        
        return jsonify({
            'success': True,
            'solution': solution['solution'],
            'metadata': {
                'subject': subject,
                'difficulty': difficulty,
                'timestamp': datetime.now().isoformat(),
                'enhanced_with_context': bool(context),
                'processing_status': 'completed',
                'model_used': solution.get('model_used', 'Unknown'),
                'confidence': solution.get('confidence', 'high'),
                'processing_time': solution.get('processing_time', 0)
            }
        })
        
    except Exception as e:
        logger.error(f"Error in solve_problem: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred while processing your request. Please try again.',
            'error_type': 'internal_server_error'
        }), 500

@api_bp.route('/ai-health', methods=['GET'])
def ai_health_check():
    """Check the health status of all AI services"""
    try:
        logger.info("Request: GET /api/ai-health")
        health_status = current_app.ai_service.health_check()
        
        status_code = 200 if health_status['overall_status'] else 503
        
        return jsonify({
            'success': True,
            'status': health_status,
            'timestamp': datetime.now().isoformat()
        }), status_code
        
    except Exception as e:
        logger.error(f"Error in ai_health_check: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Unable to check AI service health',
            'status': {'overall': 'unknown'},
            'timestamp': datetime.now().isoformat()
        }), 500

@api_bp.route('/explain', methods=['POST'])
def explain_concept():
    """
    Explain a STEM concept using NVIDIA AI
    
    Expected JSON payload:
    {
        "concept": "concept name",
        "subject": "subject area",
        "level": "beginner|intermediate|advanced",
        "includeExamples": true|false,
        "includeHistory": true|false,
        "temperature": 0.3
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'concept' not in data:
            return jsonify({'error': 'Concept is required'}), 400
        
        concept = data['concept'].strip()
        if not concept:
            return jsonify({'error': 'Concept cannot be empty'}), 400
        
        # Extract parameters with defaults
        subject = data.get('subject', 'General')
        level = data.get('level', 'intermediate')
        include_examples = data.get('includeExamples', True)
        include_history = data.get('includeHistory', False)
        temperature = data.get('temperature', 0.3)
        
        # Call AI service for concept explanation
        try:
            explanation = current_app.ai_service.explain_concept(
                concept=concept,
                subject=subject,
                level=level,
                include_examples=include_examples,
                include_history=include_history,
                temperature=temperature
            )
            
            # Log the request
            logger.info(f"Concept explained successfully: {concept} in {subject}")
            
            return jsonify({
                'success': True,
                'explanation': explanation,
                'metadata': {
                    'concept': concept,
                    'subject': subject,
                    'level': level,
                    'timestamp': datetime.now().isoformat()
                }
            })
            
        except Exception as ai_error:
            logger.warning(f"AI service failed for concept explanation: {str(ai_error)}")
            
            # Check if it's a rate limiting error
            if "429" in str(ai_error) or "Service tier capacity exceeded" in str(ai_error) or "rate" in str(ai_error).lower():
                logger.info(f"Rate limit detected, using fallback service for concept: {concept}")
                
                # Use fallback service
                fallback_result = FallbackService.get_sample_explanation(concept, subject, level)
                
                return jsonify({
                    'success': True,
                    'explanation': fallback_result['explanation'],
                    'metadata': fallback_result['metadata']
                })
            else:
                # For other errors, still try fallback but log as error
                logger.error(f"AI service error, using fallback: {str(ai_error)}")
                fallback_result = FallbackService.get_sample_explanation(concept, subject, level)
                
                return jsonify({
                    'success': True,
                    'explanation': fallback_result['explanation'],
                    'metadata': fallback_result['metadata']
                })
        
    except Exception as e:
        logger.error(f"Error in explain_concept: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/formulas', methods=['POST'])
def get_formulas():
    """
    Get formula reference using NVIDIA Nemotron AI
    
    Expected JSON payload:
    {
        "subject": "subject area",
        "topic": "specific topic",
        "searchTerm": "optional search term",
        "temperature": 0.1
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'subject' not in data:
            return jsonify({'error': 'Subject is required'}), 400
        
        subject = data['subject'].strip()
        topic = data.get('topic', 'General').strip()
        search_term = data.get('searchTerm', '').strip()
        temperature = data.get('temperature', 0.1)
        
        if not subject:
            return jsonify({'error': 'Subject cannot be empty'}), 400
        
        # Call AI service for formulas
        try:
            formulas = current_app.ai_service.get_formulas(
                subject=subject,
                topic=topic,
                search_term=search_term,
                temperature=temperature
            )
            
            # Log the request
            logger.info(f"Formulas generated successfully for {subject} - {topic}")
            
            return jsonify({
                'success': True,
                'formulas': formulas,
                'metadata': {
                    'subject': subject,
                    'topic': topic,
                    'searchTerm': search_term,
                    'timestamp': datetime.now().isoformat()
                }
            })
            
        except Exception as ai_error:
            logger.warning(f"AI service failed for formulas: {str(ai_error)}")
            
            # Check if it's a rate limiting error
            if "429" in str(ai_error) or "Service tier capacity exceeded" in str(ai_error) or "rate" in str(ai_error).lower():
                logger.info(f"Rate limit detected, using fallback service for {subject} - {topic}")
                
                # Use fallback service
                fallback_result = FallbackService.get_sample_formulas(subject, topic, search_term)
                
                return jsonify({
                    'success': True,
                    'formulas': fallback_result['formulas'],
                    'metadata': fallback_result['metadata']
                })
            else:
                # For other errors, still try fallback but log as error
                logger.error(f"AI service error, using fallback: {str(ai_error)}")
                fallback_result = FallbackService.get_sample_formulas(subject, topic, search_term)
                
                return jsonify({
                    'success': True,
                    'formulas': fallback_result['formulas'],
                    'metadata': fallback_result['metadata']
                })
        
    except Exception as e:
        logger.error(f"Error in get_formulas: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/health/ai', methods=['GET'])
def health_check_ai():
    """
    Health check endpoint for all AI services
    Tests connectivity, DNS resolution, and API authentication
    """
    try:
        logger.info("Starting AI services health check")
        
        # Perform comprehensive health check
        health_status = current_app.ai_service.health_check()
        
        if health_status['overall_status']:
            logger.info("AI services health check: PASSED")
            return jsonify({
                'success': True,
                'status': 'healthy',
                'services': health_status,
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            logger.warning(f"AI services health check: DEGRADED - {health_status}")
            return jsonify({
                'success': False,
                'status': 'degraded',
                'services': health_status,
                'timestamp': datetime.now().isoformat()
            }), 503
            
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@api_bp.route('/study-tips', methods=['POST'])
def get_study_tips():
    """
    Get personalized study tips using NVIDIA Nemotron AI
    
    Expected JSON payload:
    {
        "subject": "subject area",
        "learningStyle": "learning style",
        "studyGoal": "study goal",
        "challenges": ["challenge1", "challenge2"],
        "temperature": 0.3
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'subject' not in data:
            return jsonify({'error': 'Subject is required'}), 400
        
        subject = data['subject'].strip()
        learning_style = data.get('learningStyle', 'Visual').strip()
        study_goal = data.get('studyGoal', 'General Understanding').strip()
        challenges = data.get('challenges', [])
        temperature = data.get('temperature', 0.3)
        
        if not subject:
            return jsonify({'error': 'Subject cannot be empty'}), 400
        
        # Call AI service for study tips
        try:
            tips = current_app.ai_service.get_study_tips(
                subject=subject,
                learning_style=learning_style,
                study_goal=study_goal,
                challenges=challenges,
                temperature=temperature
            )
            
            # Log the request
            logger.info(f"Study tips generated successfully for {subject}")
            
            return jsonify({
                'success': True,
                'tips': tips,
                'metadata': {
                    'subject': subject,
                    'learningStyle': learning_style,
                    'studyGoal': study_goal,
                    'challenges': challenges,
                    'timestamp': datetime.now().isoformat()
                }
            })
            
        except Exception as ai_error:
            logger.warning(f"AI service failed for study tips: {str(ai_error)}")
            
            # Check if it's a rate limiting error
            if "429" in str(ai_error) or "Service tier capacity exceeded" in str(ai_error) or "rate" in str(ai_error).lower():
                logger.info(f"Rate limit detected, using fallback service for study tips: {subject}")
                
                # Use fallback service
                fallback_result = FallbackService.get_sample_study_tips(subject, learning_style, study_goal, challenges)
                
                return jsonify({
                    'success': True,
                    'tips': fallback_result['tips'],
                    'metadata': fallback_result['metadata']
                })
            else:
                # For other errors, still try fallback but log as error
                logger.error(f"AI service error, using fallback: {str(ai_error)}")
                fallback_result = FallbackService.get_sample_study_tips(subject, learning_style, study_goal, challenges)
                
                return jsonify({
                    'success': True,
                    'tips': fallback_result['tips'],
                    'metadata': fallback_result['metadata']
                })
        
    except Exception as e:
        logger.error(f"Error in get_study_tips: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/datasets', methods=['GET'])
def get_available_datasets():
    """Get list of available datasets"""
    try:
        datasets = current_app.data_service.get_available_datasets()
        
        return jsonify({
            'success': True,
            'datasets': datasets,
            'count': len(datasets)
        })
        
    except Exception as e:
        logger.error(f"Error in get_available_datasets: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/search-problems', methods=['POST'])
def search_problems():
    """
    Search for problems in the dataset
    
    Expected JSON payload:
    {
        "subject": "subject area",
        "difficulty": "optional difficulty",
        "topic": "optional topic",
        "limit": 10
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'subject' not in data:
            return jsonify({'error': 'Subject is required'}), 400
        
        subject = data['subject'].strip()
        difficulty = data.get('difficulty', '').strip()
        topic = data.get('topic', '').strip()
        limit = data.get('limit', 10)
        
        # Search problems
        problems = current_app.data_service.search_problems(
            subject=subject,
            difficulty=difficulty if difficulty else None,
            topic=topic if topic else None,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'problems': problems,
            'count': len(problems),
            'metadata': {
                'subject': subject,
                'difficulty': difficulty,
                'topic': topic,
                'limit': limit
            }
        })
        
    except Exception as e:
        logger.error(f"Error in search_problems: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/generate-image', methods=['POST'])
def generate_image():
    """
    Generate image using Pollinations API with subject restriction
    
    Expected JSON payload:
    {
        "prompt": "image description",
        "context": "optional context",
        "size": "1024x1024",
        "quality": "standard|hd",
        "style": "vivid|natural",
        "subject": "Mathematics|Physics|Chemistry|Biology|General Science"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt is required'}), 400
        
        prompt = data['prompt'].strip()
        if not prompt:
            return jsonify({'error': 'Prompt cannot be empty'}), 400
        
        context = data.get('context', '')
        size = data.get('size', '1024x1024')
        quality = data.get('quality', 'standard')
        style = data.get('style', 'vivid')
        subject = data.get('subject', 'General Science')
        
        logger.info(f"Generating image with prompt: {prompt[:100]}... (Subject: {subject})")
        
        result = current_app.ai_service.generate_image(
            prompt=prompt,
            context=context,
            size=size,
            quality=quality,
            style=style,
            subject=subject
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'image_url': result['image_url'],
                'revised_prompt': result.get('revised_prompt'),
                'model': result['model'],
                'metadata': {
                    'original_prompt': prompt,
                    'enhanced_prompt': result.get('enhanced_prompt'),
                    'size': size,
                    'quality': quality,
                    'style': style,
                    'subject': subject,
                    'timestamp': datetime.now().isoformat()
                }
            })
        else:
            # Check if it's a subject mismatch error
            if result.get('error') == 'subject_mismatch':
                return jsonify({
                    'success': False,
                    'error': 'subject_mismatch',
                    'message': result.get('message'),
                    'detected_subject': result.get('detected_subject'),
                    'selected_subject': result.get('selected_subject')
                }), 400
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error')
            }), 500
        
    except Exception as e:
        logger.error(f"Error in generate_image: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/generate-diagram', methods=['POST'])
def generate_educational_diagram():
    """
    Generate educational diagram for STEM concepts
    
    Expected JSON payload:
    {
        "concept": "concept name",
        "subject": "Physics|Chemistry|Mathematics|Biology|Computer Science",
        "difficulty": "beginner|intermediate|advanced"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'concept' not in data:
            return jsonify({'error': 'Concept is required'}), 400
        
        concept = data['concept'].strip()
        if not concept:
            return jsonify({'error': 'Concept cannot be empty'}), 400
        
        subject = data.get('subject', 'General')
        difficulty = data.get('difficulty', 'intermediate')
        
        logger.info(f"Generating educational diagram for: {concept} in {subject}")
        
        result = current_app.ai_service.generate_educational_diagram(
            concept=concept,
            subject=subject,
            difficulty=difficulty
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'image_url': result['image_url'],
                'revised_prompt': result.get('revised_prompt'),
                'model': result['model'],
                'metadata': {
                    'concept': concept,
                    'subject': subject,
                    'difficulty': difficulty,
                    'timestamp': datetime.now().isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
    except Exception as e:
        logger.error(f"Error in generate_educational_diagram: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/generate-problem-illustration', methods=['POST'])
def generate_problem_illustration():
    """
    Generate illustration for STEM problems
    
    Expected JSON payload:
    {
        "problem": "problem statement",
        "subject": "subject area"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'problem' not in data:
            return jsonify({'error': 'Problem statement is required'}), 400
        
        problem = data['problem'].strip()
        if not problem:
            return jsonify({'error': 'Problem statement cannot be empty'}), 400
        
        subject = data.get('subject', 'General')
        
        logger.info(f"Generating problem illustration for {subject} problem")
        
        result = current_app.ai_service.generate_problem_illustration(
            problem_text=problem,
            subject=subject
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'image_url': result['image_url'],
                'revised_prompt': result.get('revised_prompt'),
                'model': result['model'],
                'metadata': {
                    'problem': problem[:200] + '...' if len(problem) > 200 else problem,
                    'subject': subject,
                    'timestamp': datetime.now().isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
    except Exception as e:
        logger.error(f"Error in generate_problem_illustration: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/analyze-image', methods=['POST'])
def analyze_image():
    """
    Analyze image using GPT-4 Vision
    
    Expected JSON payload:
    {
        "image_url": "url to image",
        "question": "optional question about the image"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'image_url' not in data:
            return jsonify({'error': 'Image URL is required'}), 400
        
        image_url = data['image_url'].strip()
        if not image_url:
            return jsonify({'error': 'Image URL cannot be empty'}), 400
        
        question = data.get('question', '')
        
        logger.info(f"Analyzing image: {image_url}")
        
        result = current_app.ai_service.analyze_image(
            image_url=image_url,
            question=question
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'analysis': result['analysis'],
                'model': result['model'],
                'metadata': {
                    'image_url': image_url,
                    'question': question,
                    'timestamp': datetime.now().isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
        
    except Exception as e:
        logger.error(f"Error in analyze_image: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/image-training-stats', methods=['GET'])
def get_image_training_stats():
    """Get statistics about image training data"""
    try:
        stats = current_app.ai_service.get_image_training_stats()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in get_image_training_stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/create-fine-tuning-dataset', methods=['POST'])
def create_fine_tuning_dataset():
    """Create fine-tuning dataset from image training data"""
    try:
        result = current_app.ai_service.create_fine_tuning_dataset()
        
        return jsonify({
            'success': result['success'],
            'message': result.get('message', ''),
            'dataset_path': result.get('dataset_path', ''),
            'entries_count': result.get('entries_count', 0),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in create_fine_tuning_dataset: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/transcribe-audio', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio to text using Deepgram API with dataset enhancement
    
    Expected JSON payload:
    {
        "audio": "base64_encoded_audio_data",
        "format": "wav",
        "options": {
            "model": "nova-2",
            "language": "en-US",
            "punctuate": true,
            "smart_format": true
        }
    }
    
    OR multipart/form-data with audio file
    """
    try:
        logger.info("Request: POST /api/transcribe-audio")
        
        # Import voice service
        voice_service = current_app.voice_service
        if not voice_service:
            return jsonify({
                'success': False,
                'error': 'Voice service not available'
            }), 503
        
        audio_data = None
        options = {}
        
        # Handle JSON request with base64 audio
        if request.is_json:
            data = request.get_json()
            if not data or 'audio' not in data:
                return jsonify({
                    'success': False,
                    'error': 'Base64 audio data is required'
                }), 400
            
            # Handle format conversion
            audio_format = data.get('format', 'webm')
            content_type_map = {
                'wav': 'audio/wav',
                'webm': 'audio/webm',
                'mp4': 'audio/mp4',
                'ogg': 'audio/ogg'
            }
            
            options = data.get('options', {})
            options['content_type'] = content_type_map.get(audio_format, 'audio/webm')
            
            result = voice_service.transcribe_base64_audio(data['audio'], options)
        
        # Handle file upload
        elif 'audio' in request.files:
            audio_file = request.files['audio']
            if audio_file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No audio file provided'
                }), 400
            
            audio_data = audio_file.read()
            options = request.form.get('options', {})
            if isinstance(options, str):
                import json
                try:
                    options = json.loads(options)
                except:
                    options = {}
            
            result = voice_service.transcribe_audio(audio_data, options)
        
        else:
            return jsonify({
                'success': False,
                'error': 'Audio data must be provided as base64 string or file upload'
            }), 400
        
        # Add response metadata
        result['timestamp'] = datetime.now().isoformat()
        result['api_version'] = '1.0'
        
        if result['success']:
            logger.info(f"Transcription successful: {len(result['transcript'])} characters")
            return jsonify(result)
        else:
            logger.error(f"Transcription failed: {result.get('error', 'Unknown error')}")
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error in transcribe_audio: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@api_bp.route('/voice-search', methods=['POST'])
def voice_search():
    """
    Search for similar audio samples in training dataset
    
    Expected JSON payload:
    {
        "query": "text to search for",
        "limit": 5
    }
    """
    try:
        logger.info("Request: POST /api/voice-search")
        
        voice_service = current_app.voice_service
        if not voice_service:
            return jsonify({
                'success': False,
                'error': 'Voice service not available'
            }), 503
        
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        query = data['query'].strip()
        limit = data.get('limit', 5)
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query cannot be empty'
            }), 400
        
        # Search for similar samples
        results = voice_service.search_similar_audio_samples(query, limit)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'count': len(results),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in voice_search: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/voice-training-stats', methods=['GET'])
def get_voice_training_stats():
    """Get statistics about the voice training dataset"""
    try:
        logger.info("Request: GET /api/voice-training-stats")
        
        voice_service = current_app.voice_service
        if not voice_service:
            return jsonify({
                'success': False,
                'error': 'Voice service not available'
            }), 503
        
        stats = voice_service.get_training_stats()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in get_voice_training_stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/solve-with-voice', methods=['POST'])
def solve_with_voice():
    """
    Solve problem from voice input - combines transcription and problem solving
    
    Expected JSON payload:
    {
        "audio": "base64_encoded_audio_data",
        "subject": "Physics|Chemistry|Mathematics|Biology|Computer Science",
        "difficulty": "Beginner|Intermediate|Advanced|University|Graduate",
        "showSteps": true|false,
        "includeTheory": true|false,
        "includeDiagrams": true|false
    }
    """
    try:
        logger.info("Request: POST /api/solve-with-voice")
        
        voice_service = current_app.voice_service
        if not voice_service:
            return jsonify({
                'success': False,
                'error': 'Voice service not available'
            }), 503
        
        data = request.get_json()
        if not data or 'audio' not in data:
            return jsonify({
                'success': False,
                'error': 'Audio data is required'
            }), 400
        
        # Step 1: Transcribe audio
        transcription_result = voice_service.transcribe_base64_audio(data['audio'])
        
        if not transcription_result['success']:
            return jsonify({
                'success': False,
                'error': f"Transcription failed: {transcription_result.get('error', 'Unknown error')}",
                'step': 'transcription'
            }), 500
        
        transcript = transcription_result['transcript']
        if not transcript.strip():
            return jsonify({
                'success': False,
                'error': 'No speech detected in audio',
                'step': 'transcription'
            }), 400
        
        # Step 2: Solve the transcribed problem
        solve_data = {
            'problem': transcript,
            'subject': data.get('subject', 'Mathematics'),
            'difficulty': data.get('difficulty', 'Intermediate'),
            'showSteps': data.get('showSteps', True),
            'includeTheory': data.get('includeTheory', True),
            'includeDiagrams': data.get('includeDiagrams', True)
        }
        
        # Get solution from AI service
        result = current_app.ai_service.solve_problem(
            problem=solve_data['problem'],
            subject=solve_data['subject'],
            difficulty=solve_data['difficulty'],
            show_steps=solve_data['showSteps'],
            include_theory=solve_data['includeTheory'],
            include_diagrams=solve_data['includeDiagrams']
        )
        
        # Combine transcription and solution results
        response = {
            'success': True,
            'transcription': {
                'transcript': transcript,
                'confidence': transcription_result['confidence'],
                'enhancement_applied': transcription_result.get('enhancement_applied', False)
            },
            'solution': result,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Voice problem solved successfully: '{transcript[:50]}...'")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in solve_with_voice: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'step': 'processing'
        }), 500