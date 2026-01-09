import React, { useState } from 'react';
import { BookOpen, Loader2, Copy, Download, Target, Settings, FileText, ChevronDown, ChevronUp, RefreshCw } from 'lucide-react';
import { Button } from '../components/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/Card';
import SolutionRenderer from '../components/SolutionRenderer';
import { ApiService } from '../services/api';

const StudyTipsView = () => {
  const [subject, setSubject] = useState('General STEM');
  const [learningStyle, setLearningStyle] = useState('Visual');
  const [studyGoal, setStudyGoal] = useState('General Understanding');
  const [challenges, setChallenges] = useState([]);
  const [tips, setTips] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('input');
  const [isConfigCollapsed, setIsConfigCollapsed] = useState(false);

  const subjects = [
    'General STEM', 'Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'General Science'
  ];

  const learningStyles = [
    'Visual', 'Auditory', 'Reading/Writing', 'Kinesthetic', 'Not Sure'
  ];

  const studyGoals = [
    'General Understanding', 'Exam Preparation', 'Problem-Solving Skills',
    'Research Preparation', 'Long-term Retention', 'Career Development'
  ];

  const challengeOptions = [
    'Complex Concepts', 'Mathematical Calculations', 'Memorization',
    'Problem-Solving', 'Time Management', 'Test Anxiety',
    'Staying Motivated', 'Note Taking', 'Group Study'
  ];

  const handleChallengeChange = (challenge, checked) => {
    if (checked) {
      setChallenges([...challenges, challenge]);
    } else {
      setChallenges(challenges.filter(c => c !== challenge));
    }
  };

  const handleGetTips = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await ApiService.getStudyTips({
        subject,
        learningStyle,
        studyGoal,
        challenges,
        temperature: 0.3,
      });

      setTips(response);
      setActiveTab('tips');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (tips) {
      navigator.clipboard.writeText(tips.tips);
    }
  };

  const handleDownload = () => {
    if (tips) {
      const blob = new Blob([tips.tips], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `study-tips-${subject.replace(/\s+/g, '-')}-${Date.now()}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  // Reset all state to generate another study plan
  const handleAskAnother = () => {
    setChallenges([]);
    setTips(null);
    setError(null);
    setActiveTab('input');
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-blue-50 to-indigo-50 overflow-auto pb-20">
      <div className="max-w-7xl mx-auto p-6 space-y-6">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-r from-emerald-600 to-blue-600 rounded-full flex items-center justify-center">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">
              Study Tips
            </h1>
          </div>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Get personalized study strategies tailored to your learning style and goals
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex justify-center">
          <div className="bg-white rounded-xl p-1 shadow-lg border border-emerald-100">
            <div className="flex space-x-1">
              <button
                onClick={() => setActiveTab('input')}
                className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                  activeTab === 'input'
                    ? 'bg-gradient-to-r from-emerald-600 to-blue-600 text-white shadow-md'
                    : 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <Settings className="w-4 h-4" />
                  <span>Study Profile</span>
                </div>
              </button>
              <button
                onClick={() => setActiveTab('tips')}
                disabled={!tips}
                className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                  activeTab === 'tips' && tips
                    ? 'bg-gradient-to-r from-emerald-600 to-blue-600 text-white shadow-md'
                    : tips
                    ? 'text-gray-600 hover:text-emerald-600 hover:bg-emerald-50'
                    : 'text-gray-400 cursor-not-allowed'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <FileText className="w-4 h-4" />
                  <span>Study Plan</span>
                  {tips && (
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  )}
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="w-full">
          {activeTab === 'input' && (
            <Card className="w-full max-w-5xl mx-auto animate-fade-in">
              <CardHeader className="bg-gradient-to-r from-emerald-50 to-blue-50 border-b border-emerald-200/50">
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center space-x-2">
                    <div className="w-8 h-8 bg-gradient-to-r from-emerald-600 to-blue-600 rounded-lg flex items-center justify-center">
                      <BookOpen className="h-4 w-4 text-white" />
                    </div>
                    <span className="text-emerald-800">Your Study Profile</span>
                  </CardTitle>
                  <button
                    onClick={() => setIsConfigCollapsed(!isConfigCollapsed)}
                    className="text-emerald-600 hover:text-emerald-700 transition-colors"
                  >
                    {isConfigCollapsed ? <ChevronDown className="w-5 h-5" /> : <ChevronUp className="w-5 h-5" />}
                  </button>
                </div>
              </CardHeader>
              <CardContent className={`transition-all duration-300 ${isConfigCollapsed ? 'p-4' : 'p-8'}`}>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  {/* Left Column - Basic Settings */}
                  <div className="space-y-6">
                    <div className="bg-emerald-50 rounded-xl p-6 space-y-4">
                      <h3 className="text-lg font-semibold text-emerald-800">Basic Info</h3>
                      
                      <div>
                        <label className="text-sm font-medium text-emerald-700 block mb-2">Subject</label>
                        <select
                          value={subject}
                          onChange={(e) => setSubject(e.target.value)}
                          className="w-full p-3 border border-emerald-200 rounded-lg bg-white focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
                        >
                          {subjects.map((s) => (
                            <option key={s} value={s}>{s}</option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <label className="text-sm font-medium text-emerald-700 block mb-2">Learning Style</label>
                        <select
                          value={learningStyle}
                          onChange={(e) => setLearningStyle(e.target.value)}
                          className="w-full p-3 border border-emerald-200 rounded-lg bg-white focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
                        >
                          {learningStyles.map((style) => (
                            <option key={style} value={style}>{style}</option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <label className="text-sm font-medium text-emerald-700 block mb-2">Study Goal</label>
                        <select
                          value={studyGoal}
                          onChange={(e) => setStudyGoal(e.target.value)}
                          className="w-full p-3 border border-emerald-200 rounded-lg bg-white focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all"
                        >
                          {studyGoals.map((goal) => (
                            <option key={goal} value={goal}>{goal}</option>
                          ))}
                        </select>
                      </div>
                    </div>
                  </div>

                  {/* Middle Column - Challenges */}
                  <div className="space-y-6">
                    <div className="bg-blue-50 rounded-xl p-6 space-y-4">
                      <h3 className="text-lg font-semibold text-blue-800">Study Challenges</h3>
                      <p className="text-sm text-gray-600">
                        Select any challenges you're facing (optional)
                      </p>
                      
                      <div className="grid grid-cols-1 gap-2">
                        {challengeOptions.map((challenge) => (
                          <label key={challenge} className="flex items-center space-x-3 p-2 rounded-lg hover:bg-white/50 transition-colors">
                            <input
                              type="checkbox"
                              checked={challenges.includes(challenge)}
                              onChange={(e) => handleChallengeChange(challenge, e.target.checked)}
                              className="w-4 h-4 rounded border-blue-300 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="text-sm text-gray-700">{challenge}</span>
                          </label>
                        ))}
                      </div>

                      {challenges.length > 0 && (
                        <div className="mt-4 p-3 bg-white/50 rounded-lg">
                          <p className="text-xs text-gray-600 mb-2">Selected challenges:</p>
                          <div className="flex flex-wrap gap-1">
                            {challenges.map((challenge) => (
                              <span
                                key={challenge}
                                className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full font-medium"
                              >
                                {challenge}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Right Column - Action */}
                  <div className="space-y-6">
                    <div className="bg-gradient-to-br from-emerald-50 to-blue-50 rounded-xl p-6 space-y-6 text-center">
                      <div className="w-16 h-16 bg-gradient-to-r from-emerald-600 to-blue-600 rounded-full flex items-center justify-center mx-auto">
                        <Target className="w-8 h-8 text-white" />
                      </div>
                      
                      <div className="space-y-2">
                        <h3 className="text-xl font-semibold text-gray-800">
                          Ready to Get Tips?
                        </h3>
                        <p className="text-sm text-gray-600">
                          Generate personalized study strategies based on your profile
                        </p>
                      </div>

                      <Button
                        onClick={handleGetTips}
                        disabled={loading}
                        className="w-full h-14 text-lg font-semibold bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {loading ? (
                          <>
                            <Loader2 className="h-6 w-6 mr-3 animate-spin" />
                            Generating Tips...
                          </>
                        ) : (
                          <>
                            <Target className="h-6 w-6 mr-3" />
                            Get Study Tips
                          </>
                        )}
                      </Button>

                      {error && (
                        <div className="p-4 bg-red-50 border-l-4 border-red-500 rounded-lg text-left">
                          <div className="flex items-center space-x-2">
                            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                            <span className="font-semibold text-red-700">Error</span>
                          </div>
                          <p className="mt-2 text-red-600 text-sm">{error}</p>
                        </div>
                      )}

                      {/* Quick Tips Preview */}
                      <div className="bg-white/50 rounded-lg p-4 text-left">
                        <h4 className="text-sm font-semibold text-gray-700 mb-2">Quick Study Tips</h4>
                        <ul className="text-xs text-gray-600 space-y-1">
                          <li>• Use the Pomodoro Technique (25 min study, 5 min break)</li>
                          <li>• Practice active recall instead of passive reading</li>
                          <li>• Create mind maps for complex concepts</li>
                          <li>• Teach concepts to others to test understanding</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {activeTab === 'tips' && tips && (
            <div className="w-full animate-fade-in">
              {/* Floating Action Bar */}
              <div className="sticky top-4 z-10 mb-6">
                <div className="bg-white/90 backdrop-blur-sm rounded-xl border border-emerald-100 shadow-lg p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                        <span className="text-sm font-medium text-gray-700">
                          Study Plan Ready
                        </span>
                      </div>
                      <div className="text-sm text-gray-500">
                        {new Date(tips.metadata.timestamp).toLocaleString()}
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleCopy}
                        className="border-emerald-200 text-emerald-600 hover:bg-emerald-50"
                      >
                        <Copy className="h-4 w-4 mr-1" />
                        Copy
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleDownload}
                        className="border-emerald-200 text-emerald-600 hover:bg-emerald-50"
                      >
                        <Download className="h-4 w-4 mr-1" />
                        Download
                      </Button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Study Tips Content */}
              <Card className="w-full">
                <CardHeader className="bg-gradient-to-r from-emerald-50 to-blue-50 border-b border-emerald-200/50">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center space-x-2 text-xl">
                        <div className="w-8 h-8 bg-gradient-to-r from-emerald-600 to-blue-600 rounded-lg flex items-center justify-center">
                          <BookOpen className="h-4 w-4 text-white" />
                        </div>
                        <span className="text-emerald-800">Personalized Study Plan</span>
                      </CardTitle>
                      <Button
                        onClick={handleAskAnother}
                        className="bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-700 hover:to-blue-700 text-white px-4 py-2 shadow-md hover:shadow-lg transition-all duration-200"
                      >
                        <RefreshCw className="w-4 h-4 mr-2" />
                        Generate Another
                      </Button>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <span className="bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full text-sm font-medium">
                        {tips.metadata.subject}
                      </span>
                      <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                        {tips.metadata.learningStyle}
                      </span>
                      <span className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium">
                        {tips.metadata.studyGoal}
                      </span>
                      {tips.metadata.challenges && tips.metadata.challenges.length > 0 && (
                        <span className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm font-medium">
                          {tips.metadata.challenges.length} Challenge{tips.metadata.challenges.length > 1 ? 's' : ''}
                        </span>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="p-8">
                  <SolutionRenderer solution={tips.tips} />
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === 'tips' && !tips && (
            <Card className="w-full max-w-2xl mx-auto">
              <CardContent className="p-12">
                <div className="text-center space-y-4">
                  <BookOpen className="h-16 w-16 mx-auto text-gray-400" />
                  <h3 className="text-xl font-semibold text-gray-700">
                    No Study Plan Yet
                  </h3>
                  <p className="text-gray-500">
                    Complete your study profile and generate personalized tips first.
                  </p>
                  <Button
                    onClick={() => setActiveTab('input')}
                    className="mt-4"
                  >
                    Create Study Profile
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default StudyTipsView;
