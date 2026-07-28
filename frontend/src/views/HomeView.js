import React, { useState, useEffect } from 'react';
import { 
  Brain, Mic, Lightbulb, Calculator, BookOpen, Image, 
  Sparkles, Atom, FlaskConical, Dna, Code, Rocket,
  Zap, Target, Award, ArrowRight, ChevronRight,
  GraduationCap, Globe
} from 'lucide-react';

const HomeView = ({ onViewChange }) => {
  const [animatedStats, setAnimatedStats] = useState({ subjects: 0, features: 0, models: 0 });
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
    // Animate stats counter
    const duration = 2000;
    const steps = 60;
    const interval = duration / steps;
    
    const targets = { subjects: 5, features: 6, models: 3 };
    let step = 0;
    
    const timer = setInterval(() => {
      step++;
      const progress = Math.min(step / steps, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
      
      setAnimatedStats({
        subjects: Math.round(targets.subjects * eased),
        features: Math.round(targets.features * eased),
        models: Math.round(targets.models * eased),
      });
      
      if (step >= steps) clearInterval(timer);
    }, interval);
    
    return () => clearInterval(timer);
  }, []);

  const features = [
    {
      id: 'solver',
      title: 'Problem Solver',
      description: 'Get step-by-step solutions to complex STEM problems with detailed explanations powered by Together.ai.',
      icon: Brain,
      gradient: 'from-blue-500 to-indigo-600',
      shadowColor: 'shadow-blue-500/25',
      delay: '0ms',
    },
    {
      id: 'voice',
      title: 'Voice Input',
      description: 'Speak your questions naturally using AssemblyAI-powered voice recognition. Perfect for hands-free learning.',
      icon: Mic,
      gradient: 'from-teal-500 to-cyan-600',
      shadowColor: 'shadow-teal-500/25',
      delay: '100ms',
    },
    {
      id: 'explainer',
      title: 'Concept Explainer',
      description: 'Get clear explanations of complex concepts tailored to your learning level — beginner to advanced.',
      icon: Lightbulb,
      gradient: 'from-amber-500 to-orange-600',
      shadowColor: 'shadow-amber-500/25',
      delay: '200ms',
    },
    {
      id: 'formulas',
      title: 'Formula Reference',
      description: 'Quick access to important formulas organized by subject and topic. Never forget a formula again.',
      icon: Calculator,
      gradient: 'from-purple-500 to-pink-600',
      shadowColor: 'shadow-purple-500/25',
      delay: '300ms',
    },
    {
      id: 'study',
      title: 'Study Tips',
      description: 'Personalized study strategies based on your learning style, goals, and challenges.',
      icon: BookOpen,
      gradient: 'from-emerald-500 to-green-600',
      shadowColor: 'shadow-emerald-500/25',
      delay: '400ms',
    },
    {
      id: 'images',
      title: 'AI Images',
      description: 'Generate educational diagrams, visualizations, and concept illustrations using multiple AI models.',
      icon: Image,
      gradient: 'from-rose-500 to-red-600',
      shadowColor: 'shadow-rose-500/25',
      delay: '500ms',
    },
  ];

  const subjects = [
    { name: 'Physics', icon: Atom, color: 'text-blue-500' },
    { name: 'Chemistry', icon: FlaskConical, color: 'text-emerald-500' },
    { name: 'Mathematics', icon: Calculator, color: 'text-purple-500' },
    { name: 'Biology', icon: Dna, color: 'text-rose-500' },
    { name: 'Computer Science', icon: Code, color: 'text-amber-500' },
  ];

  return (
    <div className="h-full overflow-y-auto">
      {/* Hero Section */}
      <section className="relative min-h-[85vh] flex items-center justify-center overflow-hidden px-6 py-16">
        {/* Animated Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950 transition-colors duration-500" />
        
        {/* Floating Icons */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-[10%] left-[5%] animate-float-slow opacity-10 dark:opacity-5">
            <Atom className="w-24 h-24 text-blue-500" />
          </div>
          <div className="absolute top-[20%] right-[8%] animate-float-medium opacity-10 dark:opacity-5">
            <FlaskConical className="w-20 h-20 text-emerald-500" />
          </div>
          <div className="absolute bottom-[15%] left-[10%] animate-float-fast opacity-10 dark:opacity-5">
            <Calculator className="w-16 h-16 text-purple-500" />
          </div>
          <div className="absolute bottom-[25%] right-[12%] animate-float-slow opacity-10 dark:opacity-5">
            <Dna className="w-20 h-20 text-rose-500" />
          </div>
          <div className="absolute top-[50%] left-[50%] animate-float-medium opacity-5 dark:opacity-[0.03]">
            <Code className="w-32 h-32 text-amber-500" />
          </div>
        </div>

        {/* Gradient Orbs */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-400/20 dark:bg-blue-500/10 rounded-full blur-3xl animate-pulse-soft" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-400/20 dark:bg-indigo-500/10 rounded-full blur-3xl animate-pulse-soft" style={{ animationDelay: '1s' }} />

        {/* Hero Content */}
        <div className={`relative z-10 text-center max-w-5xl mx-auto transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/80 dark:bg-white/10 backdrop-blur-sm border border-blue-200/50 dark:border-white/10 shadow-lg mb-8">
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span className="text-sm font-medium text-slate-700 dark:text-slate-300">AI-Powered STEM Education</span>
            <Sparkles className="w-4 h-4 text-amber-500" />
          </div>

          {/* Main Title */}
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            <span className="bg-gradient-to-r from-slate-900 via-blue-800 to-indigo-900 dark:from-white dark:via-blue-200 dark:to-indigo-200 bg-clip-text text-transparent">
              Learn STEM
            </span>
            <br />
            <span className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 dark:from-blue-400 dark:via-indigo-400 dark:to-purple-400 bg-clip-text text-transparent">
              Smarter & Faster
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-lg md:text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Solve complex problems, understand concepts deeply, and accelerate your learning with AI-powered tools built for students and educators.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <button
              onClick={() => onViewChange('solver')}
              className="group flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-2xl font-semibold text-lg shadow-xl shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-105 transition-all duration-300"
            >
              <Brain className="w-5 h-5" />
              Start Solving
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
            <button
              onClick={() => onViewChange('voice')}
              className="group flex items-center gap-3 px-8 py-4 bg-white/80 dark:bg-white/10 backdrop-blur-sm border-2 border-slate-200 dark:border-white/20 text-slate-700 dark:text-white rounded-2xl font-semibold text-lg hover:border-blue-400 dark:hover:border-blue-400 hover:shadow-xl hover:scale-105 transition-all duration-300"
            >
              <Mic className="w-5 h-5" />
              Try Voice Input
              <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>

          {/* Subject Pills */}
          <div className="flex flex-wrap items-center justify-center gap-3">
            {subjects.map((subject, index) => {
              const Icon = subject.icon;
              return (
                <div
                  key={subject.name}
                  className="flex items-center gap-2 px-4 py-2 bg-white/60 dark:bg-white/5 backdrop-blur-sm rounded-full border border-slate-200/50 dark:border-white/10 shadow-sm hover:shadow-md hover:scale-105 transition-all duration-300 cursor-default"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <Icon className={`w-4 h-4 ${subject.color}`} />
                  <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{subject.name}</span>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="relative py-16 px-6 bg-white/50 dark:bg-slate-900/50 backdrop-blur-sm border-y border-slate-200/50 dark:border-white/5">
        <div className="max-w-5xl mx-auto">
          <div className="grid grid-cols-3 gap-8">
            <div className="text-center group">
              <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:scale-110 transition-transform duration-300">
                <GraduationCap className="w-7 h-7 text-white" />
              </div>
              <div className="text-4xl font-bold text-slate-900 dark:text-white mb-1">{animatedStats.subjects}</div>
              <div className="text-sm text-slate-500 dark:text-slate-400 font-medium">STEM Subjects</div>
            </div>
            <div className="text-center group">
              <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-110 transition-transform duration-300">
                <Zap className="w-7 h-7 text-white" />
              </div>
              <div className="text-4xl font-bold text-slate-900 dark:text-white mb-1">{animatedStats.features}</div>
              <div className="text-sm text-slate-500 dark:text-slate-400 font-medium">AI-Powered Tools</div>
            </div>
            <div className="text-center group">
              <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center shadow-lg shadow-purple-500/20 group-hover:scale-110 transition-transform duration-300">
                <Globe className="w-7 h-7 text-white" />
              </div>
              <div className="text-4xl font-bold text-slate-900 dark:text-white mb-1">{animatedStats.models}</div>
              <div className="text-sm text-slate-500 dark:text-slate-400 font-medium">AI Models Integrated</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 bg-gradient-to-b from-slate-50 to-white dark:from-slate-900 dark:to-slate-950 transition-colors duration-500">
        <div className="max-w-6xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-50 dark:bg-blue-500/10 border border-blue-200/50 dark:border-blue-500/20 mb-4">
              <Target className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
              <span className="text-xs font-semibold text-blue-700 dark:text-blue-300 uppercase tracking-wider">Features</span>
            </div>
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white mb-4">
              Everything You Need to Excel
            </h2>
            <p className="text-lg text-slate-500 dark:text-slate-400 max-w-2xl mx-auto">
              Six powerful AI tools designed to transform how you learn, solve, and understand STEM subjects.
            </p>
          </div>

          {/* Feature Cards */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <button
                  key={feature.id}
                  onClick={() => onViewChange(feature.id)}
                  className={`group relative text-left p-6 rounded-2xl bg-white dark:bg-slate-800/50 border border-slate-200/80 dark:border-slate-700/50 shadow-sm hover:shadow-xl ${feature.shadowColor} hover:-translate-y-2 transition-all duration-300 overflow-hidden`}
                  style={{ animationDelay: feature.delay }}
                >
                  {/* Hover Gradient */}
                  <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-[0.03] dark:group-hover:opacity-[0.08] transition-opacity duration-300`} />

                  {/* Icon */}
                  <div className={`relative w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center shadow-lg ${feature.shadowColor} mb-5 group-hover:scale-110 transition-transform duration-300`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>

                  {/* Content */}
                  <h3 className="relative text-lg font-bold text-slate-900 dark:text-white mb-2 group-hover:text-blue-700 dark:group-hover:text-blue-300 transition-colors">
                    {feature.title}
                  </h3>
                  <p className="relative text-sm text-slate-500 dark:text-slate-400 leading-relaxed mb-4">
                    {feature.description}
                  </p>

                  {/* Arrow */}
                  <div className="relative flex items-center gap-1 text-sm font-semibold text-blue-600 dark:text-blue-400 group-hover:gap-2 transition-all">
                    <span>Explore</span>
                    <ArrowRight className="w-4 h-4" />
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </section>

      {/* Powered By Section */}
      <section className="py-16 px-6 bg-white dark:bg-slate-950 border-t border-slate-200/50 dark:border-white/5 transition-colors duration-500">
        <div className="max-w-4xl mx-auto text-center">
          <p className="text-sm font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-8">
            Powered by Industry-Leading AI
          </p>
          <div className="flex flex-wrap items-center justify-center gap-10">
            <div className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-md group-hover:scale-110 transition-transform">
                <Rocket className="w-5 h-5 text-white" />
              </div>
              <div className="text-left">
                <div className="text-sm font-bold text-slate-800 dark:text-slate-200">Together.ai</div>
                <div className="text-xs text-slate-400 dark:text-slate-500">Problem Solving</div>
              </div>
            </div>
            <div className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center shadow-md group-hover:scale-110 transition-transform">
                <Image className="w-5 h-5 text-white" />
              </div>
              <div className="text-left">
                <div className="text-sm font-bold text-slate-800 dark:text-slate-200">Pollinations.ai</div>
                <div className="text-xs text-slate-400 dark:text-slate-500">Image Generation</div>
              </div>
            </div>
            <div className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center shadow-md group-hover:scale-110 transition-transform">
                <Mic className="w-5 h-5 text-white" />
              </div>
              <div className="text-left">
                <div className="text-sm font-bold text-slate-800 dark:text-slate-200">AssemblyAI</div>
                <div className="text-xs text-slate-400 dark:text-slate-500">Voice Recognition</div>
              </div>
            </div>
          </div>
          
          {/* Footer */}
          <div className="mt-16 pt-8 border-t border-slate-100 dark:border-white/5">
            <div className="flex items-center justify-center gap-2 mb-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-lg flex items-center justify-center">
                <Brain className="w-4 h-4 text-white" />
              </div>
              <span className="text-lg font-bold text-slate-800 dark:text-slate-200">STEMCatalyst</span>
            </div>
            <p className="text-sm text-slate-400 dark:text-slate-500">
              Built by <span className="font-semibold text-slate-600 dark:text-slate-300">Senaaravichandran A</span> • Flaunch Internship Program
            </p>
            <div className="flex items-center justify-center gap-2 mt-2">
              <Award className="w-4 h-4 text-amber-500" />
              <span className="text-xs text-slate-400 dark:text-slate-500">Generative AI Intern Project</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomeView;
