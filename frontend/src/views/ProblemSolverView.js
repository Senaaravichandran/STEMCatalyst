import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Download, Copy, Brain, Image, FlaskConical, Calculator, Dna, Code, ChevronUp, Sparkles, Atom, Rocket, Lightbulb, Zap, Target, Award, RefreshCw, AlertCircle } from 'lucide-react';
import VoiceInputButton from '../components/VoiceInputButton';
import SolutionRenderer from '../components/SolutionRenderer';
import { ApiService } from '../services/api';

const ProblemSolverView = () => {
  const [problem, setProblem] = useState('');
  const [subject, setSubject] = useState('Physics');
  const [difficulty] = useState('Intermediate');
  const [showSteps] = useState(true);
  const [includeTheory] = useState(true);
  const [temperature] = useState(0.2);
  // eslint-disable-next-line no-unused-vars
  const [solution, setSolution] = useState(null);
  const [loading, setLoading] = useState(false);
  // eslint-disable-next-line no-unused-vars
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('solve');
  const [conversations, setConversations] = useState([]);
  const messagesEndRef = useRef(null);

  const subjects = [
    { id: 'Physics', label: 'Physics', icon: Atom, color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-200', gradient: 'from-blue-500 to-cyan-500' },
    { id: 'Chemistry', label: 'Chemistry', icon: FlaskConical, color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-200', gradient: 'from-emerald-500 to-teal-500' },
    { id: 'Mathematics', label: 'Mathematics', icon: Calculator, color: 'text-purple-600', bg: 'bg-purple-50', border: 'border-purple-200', gradient: 'from-purple-500 to-pink-500' },
    { id: 'Biology', label: 'Biology', icon: Dna, color: 'text-rose-600', bg: 'bg-rose-50', border: 'border-rose-200', gradient: 'from-rose-500 to-orange-500' },
    { id: 'Computer Science', label: 'Computer Science', icon: Code, color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-200', gradient: 'from-amber-500 to-yellow-500' },
  ];

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversations]);

  const handleVoiceTranscription = (transcription) => {
    setProblem(transcription);
  };

  const handleSolve = async () => {
    if (!problem.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: problem,
      subject: subject,
      mode: mode,
      timestamp: new Date()
    };

    setConversations(prev => [...prev, userMessage]);
    setProblem('');
    setLoading(true);
    setError(null);

    try {
      let response;
      if (mode === 'generate-image') {
        const res = await fetch('http://localhost:5000/api/generate-image', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            prompt: userMessage.content,
            context: `Educational ${subject} content`,
            size: '512x512',
            quality: 'standard',
            style: 'educational',
            subject: subject  // Pass selected subject for validation
          }),
        });
        const data = await res.json();
        
        // Check for subject mismatch error
        if (data.error === 'subject_mismatch') {
          throw new Error(data.message || `This image request doesn't match your selected subject (${subject}). Please select the appropriate subject or change your request.`);
        }
        
        if (data.success) {
          response = {
            type: 'image',
            imageUrl: data.image_url,
            revisedPrompt: data.enhanced_prompt || data.revised_prompt,
            model: data.model
          };
        } else {
          throw new Error(data.error || 'Failed to generate image');
        }
      } else {
        const apiResponse = await ApiService.solveProblem({
          problem: userMessage.content,
          subject,
          difficulty,
          showSteps,
          includeTheory,
          temperature,
        });
        response = {
          type: 'solution',
          solution: apiResponse.solution,
          metadata: apiResponse.metadata
        };
      }

      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: response,
        subject: subject,
        timestamp: new Date()
      };

      setConversations(prev => [...prev, aiMessage]);
      setSolution(response);
    } catch (err) {
      setError(err.message);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: err.message,
        timestamp: new Date()
      };
      setConversations(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSolve();
    }
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
  };

  const handleNewChat = () => {
    // Clear all conversations and reset state
    setConversations([]);
    setProblem('');
    setSolution(null);
    setError(null);
    setSubject('Physics');
    setMode('solve');
  };

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* Main Content Area with Right Panel */}
      <div className="flex-1 flex overflow-hidden">
        {/* Chat Area - Takes remaining space */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Messages Area - Scrollable */}
          <div className="flex-1 overflow-y-auto px-4 py-6 min-h-0">
            <div className="max-w-4xl mx-auto space-y-6">
          {/* Welcome Message */}
          {conversations.length === 0 && (
            <div className="py-8">
              {/* Hero Section */}
              <div className="text-center mb-10">
                <div className="relative inline-block mb-6">
                  <div className="w-20 h-20 bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 rounded-3xl flex items-center justify-center shadow-2xl shadow-blue-500/30 transform rotate-3 hover:rotate-0 transition-transform duration-300">
                    <Brain className="h-10 w-10 text-white" />
                  </div>
                  <div className="absolute -top-2 -right-2 w-6 h-6 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center animate-bounce">
                    <Sparkles className="h-3 w-3 text-white" />
                  </div>
                </div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-indigo-900 bg-clip-text text-transparent mb-3">
                  What can I help you solve?
                </h1>
                <p className="text-gray-500 text-lg max-w-lg mx-auto">
                  From complex equations to scientific concepts - I'm here to guide you step by step
                </p>
              </div>

              {/* Subject Cards - Creative Grid */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 max-w-4xl mx-auto mb-10">
                {subjects.map((s, index) => {
                  const Icon = s.icon;
                  return (
                    <button
                      key={s.id}
                      onClick={() => setSubject(s.id)}
                      className={`group relative p-5 rounded-2xl border-2 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 overflow-hidden ${
                        subject === s.id 
                          ? `${s.border} ${s.bg} shadow-lg` 
                          : 'border-gray-100 bg-white hover:border-gray-200'
                      }`}
                      style={{ animationDelay: `${index * 100}ms` }}
                    >
                      {/* Background Gradient on Hover */}
                      <div className={`absolute inset-0 bg-gradient-to-br ${s.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-300`}></div>
                      
                      {/* Icon Container */}
                      <div className={`relative w-12 h-12 mx-auto mb-3 rounded-xl ${s.bg} flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300`}>
                        <Icon className={`h-6 w-6 ${s.color}`} />
                      </div>
                      
                      <span className={`relative text-sm font-semibold ${subject === s.id ? s.color : 'text-gray-700 group-hover:text-gray-900'}`}>
                        {s.label}
                      </span>
                      
                      {/* Selected Indicator */}
                      {subject === s.id && (
                        <div className={`absolute top-2 right-2 w-2.5 h-2.5 bg-gradient-to-r ${s.gradient} rounded-full animate-pulse`}></div>
                      )}
                    </button>
                  );
                })}
              </div>

              {/* Quick Start Suggestions */}
              <div className="max-w-3xl mx-auto">
                <div className="flex items-center justify-center gap-2 mb-4">
                  <Lightbulb className="h-4 w-4 text-amber-500" />
                  <span className="text-sm font-medium text-gray-500">Try asking</span>
                </div>
                
                <div className="grid md:grid-cols-2 gap-3">
                  {[
                    { text: "Solve the quadratic equation x² + 5x + 6 = 0", icon: Calculator, color: 'purple', subject: 'Mathematics' },
                    { text: "Explain Newton's laws of motion", icon: Rocket, color: 'blue', subject: 'Physics' },
                    { text: "Balance: H₂ + O₂ → H₂O", icon: FlaskConical, color: 'emerald', subject: 'Chemistry' },
                    { text: "How does DNA replication work?", icon: Dna, color: 'rose', subject: 'Biology' },
                  ].map((suggestion, index) => {
                    const SuggestIcon = suggestion.icon;
                    return (
                      <button
                        key={index}
                        onClick={() => {
                          setProblem(suggestion.text);
                          setSubject(suggestion.subject);
                        }}
                        className={`group flex items-center gap-3 p-4 rounded-xl border border-gray-200 bg-white hover:bg-gray-50 hover:border-${suggestion.color}-300 hover:shadow-md transition-all duration-200 text-left`}
                      >
                        <div className={`w-10 h-10 rounded-lg bg-${suggestion.color}-50 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform`}>
                          <SuggestIcon className={`h-5 w-5 text-${suggestion.color}-600`} />
                        </div>
                        <span className="text-sm text-gray-600 group-hover:text-gray-900 line-clamp-2">
                          {suggestion.text}
                        </span>
                        <ChevronUp className="h-4 w-4 text-gray-300 rotate-90 ml-auto flex-shrink-0 group-hover:text-gray-500" />
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Stats/Features Row */}
              <div className="max-w-3xl mx-auto mt-10 pt-8 border-t border-gray-100">
                <div className="grid grid-cols-3 gap-6">
                  <div className="text-center group">
                    <div className="w-12 h-12 mx-auto mb-3 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:scale-110 transition-transform">
                      <Zap className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="font-semibold text-gray-800">Instant Solutions</h3>
                    <p className="text-xs text-gray-500 mt-1">Get answers in seconds</p>
                  </div>
                  <div className="text-center group">
                    <div className="w-12 h-12 mx-auto mb-3 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-110 transition-transform">
                      <Target className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="font-semibold text-gray-800">Step-by-Step</h3>
                    <p className="text-xs text-gray-500 mt-1">Learn the process</p>
                  </div>
                  <div className="text-center group">
                    <div className="w-12 h-12 mx-auto mb-3 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center shadow-lg shadow-purple-500/20 group-hover:scale-110 transition-transform">
                      <Award className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="font-semibold text-gray-800">Expert Quality</h3>
                    <p className="text-xs text-gray-500 mt-1">Powered by Together.ai</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Conversation Messages */}
          {conversations.map((msg) => (
            <div key={msg.id} className={`flex w-full ${msg.type === 'user' ? 'justify-end' : 'justify-start'} mb-6`}>
              {msg.type === 'user' ? (
                <div className="max-w-3xl">
                  <div className="bg-gray-100 text-gray-900 rounded-3xl px-5 py-3 shadow-sm text-base">
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                  </div>
                </div>
              ) : msg.type === 'error' ? (
                <div className="max-w-4xl w-full flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-red-100 rounded-full flex items-center justify-center mt-1">
                    <AlertCircle className="w-5 h-5 text-red-600" />
                  </div>
                  <div className="flex-1 text-red-600 text-base py-1">
                    <p className="font-medium">Error</p>
                    <p>{msg.content}</p>
                  </div>
                </div>
              ) : (
                <div className="max-w-4xl w-full flex gap-4">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mt-1 overflow-hidden border border-gray-200">
                    <Brain className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="flex-1 w-0">
                    {msg.content.type === 'image' ? (
                      <div className="space-y-3 mt-1">
                        {/* Image Container with Loading State */}
                        <div className="relative min-h-[300px] bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg overflow-hidden border border-gray-200">
                          {/* Loading overlay - shows until image loads */}
                          <div className="image-loading-overlay absolute inset-0 flex flex-col items-center justify-center z-10 bg-gradient-to-br from-blue-50 to-indigo-100">
                            <div className="relative">
                              <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
                              <Image className="absolute inset-0 m-auto h-5 w-5 text-blue-600" />
                            </div>
                            <p className="mt-4 text-sm font-medium text-blue-600 animate-pulse">Generating image...</p>
                          </div>
                          {/* Actual Image */}
                          <img 
                            src={msg.content.imageUrl} 
                            alt={msg.content.revisedPrompt}
                            className="w-full rounded-lg shadow-sm relative z-20"
                            onLoad={(e) => {
                              const overlay = e.target.parentElement.querySelector('.image-loading-overlay');
                              if (overlay) overlay.style.display = 'none';
                            }}
                          />
                        </div>
                        {msg.content.revisedPrompt && (
                          <p className="text-sm text-gray-500 italic px-2">
                            {msg.content.revisedPrompt}
                          </p>
                        )}
                      </div>
                    ) : (
                      <div className="text-base text-gray-800 leading-relaxed overflow-hidden py-1">
                        <SolutionRenderer solution={msg.content.solution} />
                      </div>
                    )}
                    <div className="flex items-center mt-3 space-x-1">
                      <button 
                        onClick={() => handleCopy(msg.content.solution || msg.content.revisedPrompt)}
                        className="p-1.5 text-gray-400 hover:text-gray-800 hover:bg-gray-100 rounded-md transition-colors"
                        title="Copy text"
                      >
                        <Copy className="h-4 w-4" />
                      </button>
                      <button 
                        className="p-1.5 text-gray-400 hover:text-gray-800 hover:bg-gray-100 rounded-md transition-colors"
                        title="Download"
                      >
                        <Download className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* Loading Indicator */}
          {loading && (
            <div className="flex w-full justify-start mb-6">
              <div className="max-w-4xl w-full flex gap-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mt-1 overflow-hidden border border-gray-200">
                  <Brain className="w-5 h-5 text-blue-600 animate-pulse" />
                </div>
                <div className="flex-1 py-1">
                  <div className="flex items-center space-x-3">
                    {mode === 'generate-image' ? (
                      <>
                        <Loader2 className="h-5 w-5 animate-spin text-purple-600" />
                        <div>
                          <span className="text-gray-700 font-medium">Generating image...</span>
                          <p className="text-xs text-gray-400">Creating your {subject} visualization</p>
                        </div>
                      </>
                    ) : (
                      <>
                        <Loader2 className="h-5 w-5 animate-spin text-blue-600" />
                        <div>
                          <span className="text-gray-700 font-medium">Solving problem...</span>
                          <p className="text-xs text-gray-400">Analyzing your {subject} question</p>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Bottom Input Bar */}
          <div className="flex-shrink-0 pt-4 pb-6 px-4">
            <div className="max-w-4xl mx-auto">
          {/* Input Box */}
          <div className="flex items-end bg-white rounded-2xl border border-gray-200 shadow-lg shadow-gray-200/50 focus-within:border-blue-400 focus-within:ring-4 focus-within:ring-blue-50 focus-within:shadow-blue-200/30 transition-all duration-200">
            {/* Text Input */}
            <textarea
              value={problem}
              onChange={(e) => setProblem(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={mode === 'generate-image' 
                ? "Describe the image you want to create..." 
                : "Ask any STEM problem..."
              }
              rows={1}
              className="flex-1 bg-transparent border-0 resize-none py-3.5 px-4 focus:outline-none focus:ring-0 max-h-32 text-gray-800 placeholder-gray-400"
              style={{ minHeight: '24px' }}
              onInput={(e) => {
                e.target.style.height = 'auto';
                e.target.style.height = Math.min(e.target.scrollHeight, 128) + 'px';
              }}
            />

            {/* Voice Input */}
            <div className="p-1.5">
              <VoiceInputButton 
                onTranscription={handleVoiceTranscription}
                isLoading={loading}
              />
            </div>

            {/* Send Button */}
            <button
              onClick={handleSolve}
              disabled={loading || !problem.trim()}
              className={`p-3 m-1.5 rounded-xl transition-all duration-200 ${
                problem.trim() && !loading
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-105'
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed'
              }`}
            >
              {loading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </button>
          </div>

          {/* Helper Text */}
          <p className="text-center text-xs text-gray-400 mt-2">
            <kbd className="px-1.5 py-0.5 bg-gray-100 rounded text-gray-500 font-mono text-xs">Enter</kbd> to send • <kbd className="px-1.5 py-0.5 bg-gray-100 rounded text-gray-500 font-mono text-xs">Shift+Enter</kbd> for new line
          </p>

          {/* New Chat Button */}
          {conversations.length > 0 && (
            <div className="flex justify-center mt-3">
              <button
                onClick={handleNewChat}
                className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-full text-sm font-medium text-gray-600 hover:text-gray-800 hover:border-gray-300 hover:shadow-md transition-all duration-200"
              >
                <RefreshCw className="h-4 w-4" />
                <span>New Chat</span>
              </button>
            </div>
          )}
          </div>
        </div>
      </div>

        {/* Right Side Panel - Fixed Width */}
        <div className="w-52 flex-shrink-0 p-4 space-y-3 overflow-y-auto border-l border-gray-100">
          {/* Subject Selector */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-3">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Subject</p>
            <div className="relative">
              <select
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="w-full appearance-none bg-gray-50 border border-gray-200 rounded-lg px-3 py-2 pr-8 text-sm font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 cursor-pointer"
              >
                {subjects.map((s) => (
                  <option key={s.id} value={s.id}>{s.label}</option>
                ))}
              </select>
              <ChevronUp className="absolute right-2 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 rotate-180 pointer-events-none" />
            </div>
          </div>

          {/* Mode Toggle */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-3">
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Mode</p>
            <div className="grid grid-cols-2 gap-1 bg-gray-100 p-1 rounded-lg">
              <button
                onClick={() => setMode('solve')}
                className={`flex items-center justify-center gap-1 py-2 px-1 rounded-md text-xs font-medium transition-all ${
                  mode === 'solve'
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Brain className="h-3.5 w-3.5" />
                <span>Solve</span>
              </button>
              <button
                onClick={() => setMode('generate-image')}
                className={`flex items-center justify-center gap-1 py-2 px-1 rounded-md text-xs font-medium transition-all ${
                  mode === 'generate-image'
                    ? 'bg-white text-purple-600 shadow-sm'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <Image className="h-3.5 w-3.5" />
                <span>Image</span>
              </button>
            </div>
          </div>

          {/* Quick Subject Icons */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-2">
            <div className="grid grid-cols-5 gap-1">
              {subjects.map((s) => {
                const Icon = s.icon;
                return (
                  <button
                    key={s.id}
                    onClick={() => setSubject(s.id)}
                    title={s.label}
                    className={`w-8 h-8 rounded-lg flex items-center justify-center transition-all ${
                      subject === s.id
                        ? `${s.bg} ${s.border} border-2 shadow-sm`
                        : 'bg-gray-50 border border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <Icon className={`h-4 w-4 ${subject === s.id ? s.color : 'text-gray-400'}`} />
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProblemSolverView;
