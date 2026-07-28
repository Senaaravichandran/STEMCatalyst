import React, { useState, useEffect } from 'react';
import { Menu, X, Brain, Calculator, BookOpen, Lightbulb, Wifi, WifiOff, Image, Mic, Home, Moon, Sun } from 'lucide-react';

import { Button } from '../components/Button';
import { cn } from '../lib/utils';
import { ApiService } from '../services/api';

const Navigation = ({ currentView, onViewChange, darkMode, onToggleDarkMode }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [isChecking, setIsChecking] = useState(true);

  const menuItems = [
    { id: 'home', label: 'Home', icon: Home, description: 'Landing page' },
    { id: 'solver', label: 'Problem Solver', icon: Brain, description: 'Solve complex problems' },
    { id: 'voice', label: 'Voice Input', icon: Mic, description: 'Speak your problems' },
    { id: 'explainer', label: 'Concept Explainer', icon: Lightbulb, description: 'Learn new concepts' },
    { id: 'formulas', label: 'Formula Reference', icon: Calculator, description: 'Quick reference guide' },
    { id: 'study', label: 'Study Tips', icon: BookOpen, description: 'Improve your study habits' },
    { id: 'images', label: 'AI Images', icon: Image, description: 'Generate AI images' },
  ];

  useEffect(() => {
    checkConnection();
    const interval = setInterval(checkConnection, 10000); // Check every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const checkConnection = async () => {
    try {
      await ApiService.healthCheck();
      setIsConnected(true);
    } catch (error) {
      setIsConnected(false);
    } finally {
      setIsChecking(false);
    }
  };

  const handleViewChange = (viewId) => {
    onViewChange(viewId);
    setIsOpen(false);
  };

  const ConnectionStatus = () => (
    <div className={cn(
      "flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-medium transition-all",
      isChecking 
        ? "bg-yellow-50 dark:bg-yellow-500/10 text-yellow-700 dark:text-yellow-400 border border-yellow-200 dark:border-yellow-500/20" 
        : isConnected 
          ? "bg-green-50 dark:bg-green-500/10 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-500/20" 
          : "bg-red-50 dark:bg-red-500/10 text-red-700 dark:text-red-400 border border-red-200 dark:border-red-500/20"
    )}>
      {isChecking ? (
        <>
          <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
          <span>Checking...</span>
        </>
      ) : isConnected ? (
        <>
          <Wifi className="h-3 w-3" />
          <span>Connected</span>
        </>
      ) : (
        <>
          <WifiOff className="h-3 w-3" />
          <span>Disconnected</span>
        </>
      )}
    </div>
  );

  return (
    <>
      {/* Mobile menu button */}
      <div className="lg:hidden fixed top-4 left-4 z-50">
        <Button
          variant="outline"
          size="icon"
          onClick={() => setIsOpen(!isOpen)}
          className="glass shadow-medium dark:bg-slate-800/80 dark:border-slate-700"
        >
          {isOpen ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
        </Button>
      </div>

      {/* Connection Status - Mobile Top Bar */}
      <div className="lg:hidden fixed top-4 right-4 z-50">
        <ConnectionStatus />
      </div>

      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={cn(
        "fixed left-0 top-0 h-screen w-72 glass-sidebar z-40 transform transition-all duration-300 ease-in-out flex flex-col shadow-xl",
        isOpen ? "translate-x-0" : "-translate-x-full",
        "lg:translate-x-0 lg:sticky lg:top-0 lg:z-0 lg:shrink-0"
      )}>
        <div className="flex flex-col h-full overflow-hidden">
          {/* Header */}
          <div className="p-4 border-b border-slate-200/50 dark:border-slate-700/50">
            <div className="flex items-center space-x-3 mb-4">
              <div className="relative">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/30 animate-glow-pulse">
                  <Brain className="h-5 w-5 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white dark:border-slate-900" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-slate-800 dark:text-white font-['Outfit']">
                  STEMCatalyst
                </h1>
                <p className="text-xs text-slate-500 dark:text-slate-400">AI Learning Assistant</p>
              </div>
            </div>
            
            {/* Connection Status */}
            <ConnectionStatus />
          </div>

          {/* Navigation - Scrollable */}
          <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
            <div className="mb-2">
              <h3 className="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wider px-3 mb-2">
                Tools
              </h3>
            </div>
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentView === item.id;

              return (
                <button
                  key={item.id}
                  onClick={() => handleViewChange(item.id)}
                  className={cn(
                    "relative w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-all duration-200 group",
                    isActive
                      ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/25"
                      : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/50"
                  )}
                >
                  {/* Active Indicator Bar */}
                  {isActive && (
                    <div className="nav-active-indicator" />
                  )}
                  
                  <Icon className={cn(
                    "h-5 w-5 shrink-0 transition-transform duration-200 group-hover:scale-110",
                    isActive ? "text-white" : "text-slate-500 dark:text-slate-400"
                  )} />
                  <div className="flex-1 text-left">
                    <div className={cn(
                      "font-medium text-sm",
                      isActive ? "text-white" : "text-slate-700 dark:text-slate-300"
                    )}>
                      {item.label}
                    </div>
                    <div className={cn(
                      "text-xs",
                      isActive ? "text-blue-100" : "text-slate-400 dark:text-slate-500"
                    )}>
                      {item.description}
                    </div>
                  </div>
                  {isActive && (
                    <div className="w-1.5 h-1.5 bg-white rounded-full" />
                  )}
                </button>
              );
            })}
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-slate-200/50 dark:border-slate-700/50 space-y-3">
            {/* Dark Mode Toggle */}
            <div className="flex items-center justify-between px-1">
              <div className="flex items-center space-x-2">
                {darkMode ? (
                  <Moon className="h-4 w-4 text-indigo-400" />
                ) : (
                  <Sun className="h-4 w-4 text-amber-500" />
                )}
                <span className="text-sm font-medium text-slate-600 dark:text-slate-300">
                  {darkMode ? 'Dark Mode' : 'Light Mode'}
                </span>
              </div>
              <button
                onClick={onToggleDarkMode}
                className="dark-mode-toggle"
                aria-label="Toggle dark mode"
              />
            </div>

            {/* Powered By */}
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center shadow-md">
                <Brain className="h-4 w-4 text-white" />
              </div>
              <div>
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Powered by Together.ai</span>
                <div className="flex items-center space-x-1">
                  <div className="w-1.5 h-1.5 bg-green-500 rounded-full" />
                  <span className="text-xs text-slate-500 dark:text-slate-400">Online</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Navigation;
