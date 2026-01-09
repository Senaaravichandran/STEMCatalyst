import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Volume2 } from 'lucide-react';

const VoiceInput = ({ onTranscription, isLoading = false, disabled = false }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [error, setError] = useState('');
  const [interimText, setInterimText] = useState('');
  const [fullTranscript, setFullTranscript] = useState('');
  
  const recognitionRef = useRef(null);
  const intervalRef = useRef(null);
  const fullTranscriptRef = useRef('');
  const isRecordingRef = useRef(false);

  // Keep refs in sync with state
  useEffect(() => {
    isRecordingRef.current = isRecording;
  }, [isRecording]);

  useEffect(() => {
    fullTranscriptRef.current = fullTranscript;
  }, [fullTranscript]);

  useEffect(() => {
    // Initialize Web Speech API
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        setInterimText(interimTranscript);

        // Accumulate final transcripts instead of sending immediately
        if (finalTranscript) {
          setFullTranscript(prev => {
            const newTranscript = prev + (prev ? ' ' : '') + finalTranscript;
            fullTranscriptRef.current = newTranscript;
            return newTranscript;
          });
        }
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        if (event.error === 'not-allowed') {
          setError('Microphone access denied. Please allow microphone access.');
        } else if (event.error === 'no-speech') {
          // Don't show error for no-speech, it's normal
          console.log('No speech detected');
        } else if (event.error === 'aborted') {
          // Aborted is normal during restart cycles, ignore it
          console.log('Recognition aborted (normal during restart)');
        } else if (event.error === 'network') {
          setError('Network error. Please check your connection.');
        } else {
          setError(`Error: ${event.error}`);
        }
      };

      recognitionRef.current.onend = () => {
        // Auto restart if still recording
        if (isRecordingRef.current && recognitionRef.current) {
          // Add a small delay before restarting to avoid rapid restart issues
          setTimeout(() => {
            if (isRecordingRef.current && recognitionRef.current) {
              try {
                recognitionRef.current.start();
              } catch (e) {
                console.log('Recognition restart failed:', e.message);
              }
            }
          }, 100);
        }
      };
    }

    return () => {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch (e) {}
      }
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  const startRecording = () => {
    if (!recognitionRef.current) {
      setError('Speech recognition not supported in this browser. Please use Chrome or Edge.');
      return;
    }

    setError('');
    setRecordingTime(0);
    setInterimText('');
    setFullTranscript('');
    fullTranscriptRef.current = '';

    try {
      recognitionRef.current.start();
      setIsRecording(true);
      
      // Start timer
      intervalRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
    } catch (err) {
      console.error('Error starting recognition:', err);
      setError('Failed to start voice input. Please try again.');
    }
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setIsRecording(false);
    setInterimText('');
    
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }

    // Send the complete transcription when recording stops
    const completeTranscript = fullTranscriptRef.current.trim();
    if (completeTranscript && onTranscription) {
      console.log('Sending complete transcript:', completeTranscript);
      onTranscription({
        transcript: completeTranscript,
        confidence: 0.9,
        enhancementApplied: false,
        metadata: { model: 'Web Speech API' }
      });
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const isSupported = !!(window.SpeechRecognition || window.webkitSpeechRecognition);

  return (
    <div className="w-full">
      {/* Main Recording Button */}
      <div className="flex flex-col items-center space-y-4">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={disabled || isLoading || !isSupported}
          className={`relative w-20 h-20 rounded-full transition-all duration-300 flex items-center justify-center ${
            isRecording
              ? 'bg-red-500 hover:bg-red-600 shadow-lg shadow-red-500/50 animate-pulse'
              : 'bg-gradient-to-br from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 shadow-lg shadow-blue-500/30'
          } ${(disabled || !isSupported) ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isRecording ? (
            <MicOff className="w-8 h-8 text-white" />
          ) : (
            <Mic className="w-8 h-8 text-white" />
          )}
          
          {/* Recording indicator ring */}
          {isRecording && (
            <div className="absolute inset-0 rounded-full border-4 border-red-300 animate-ping" />
          )}
        </button>

        {/* Status Text */}
        <div className="text-center">
          {isRecording ? (
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
              <span className="text-red-600 font-medium">Recording: {formatTime(recordingTime)}</span>
            </div>
          ) : (
            <span className="text-gray-500">Click the microphone to start voice input</span>
          )}
        </div>

        {/* Full Transcript Display (what's been captured) */}
        {isRecording && fullTranscript && (
          <div className="w-full max-w-md p-3 bg-green-50 rounded-lg border border-green-200">
            <p className="text-xs text-green-600 mb-1 font-medium">Captured:</p>
            <p className="text-green-800 text-sm">{fullTranscript}</p>
          </div>
        )}

        {/* Interim Text Display */}
        {interimText && (
          <div className="w-full max-w-md p-3 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-blue-700 text-sm italic">{interimText}...</p>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="w-full max-w-md p-3 bg-red-50 rounded-lg border border-red-200">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {/* Browser Support Warning */}
        {!isSupported && (
          <div className="w-full max-w-md p-3 bg-yellow-50 rounded-lg border border-yellow-200">
            <p className="text-yellow-700 text-sm">
              Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.
            </p>
          </div>
        )}

        {/* Enhanced badge */}
        <div className="flex items-center space-x-2 text-xs text-gray-400">
          <Volume2 className="w-4 h-4" />
          <span>Enhanced with Web Speech API</span>
        </div>
      </div>
    </div>
  );
};

export default VoiceInput;
