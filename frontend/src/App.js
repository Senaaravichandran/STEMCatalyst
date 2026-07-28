import React, { useState, useEffect } from 'react';
import Navigation from './navigation/Navigation';
import HomeView from './views/HomeView';
import ProblemSolverView from './views/ProblemSolverView';
import ConceptExplainerView from './views/ConceptExplainerView';
import FormulaReferenceView from './views/FormulaReferenceView';
import StudyTipsView from './views/StudyTipsView';
import ImageGenerator from './components/ImageGenerator';
import VoiceView from './views/VoiceView';
import ErrorBoundary from './components/ErrorBoundary';
import './index.css';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('stemcatalyst-darkmode');
    return saved ? JSON.parse(saved) : false;
  });

  // Apply dark mode class to document
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('stemcatalyst-darkmode', JSON.stringify(darkMode));
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(prev => !prev);
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case 'home':
        return <HomeView onViewChange={setCurrentView} />;
      case 'solver':
        return <ProblemSolverView />;
      case 'voice':
        return <VoiceView />;
      case 'explainer':
        return <ConceptExplainerView />;
      case 'formulas':
        return <FormulaReferenceView />;
      case 'study':
        return <StudyTipsView />;
      case 'images':
        return <ImageGenerator />;
      default:
        return <HomeView onViewChange={setCurrentView} />;
    }
  };

  return (
    <ErrorBoundary>
      <div className="h-screen overflow-hidden bg-gradient-to-br from-blue-50 via-indigo-50 to-blue-100 dark:from-slate-950 dark:via-slate-900 dark:to-indigo-950 transition-colors duration-500">
        <div className="flex h-full">
          {/* Fixed Sidebar */}
          <Navigation 
            currentView={currentView} 
            onViewChange={setCurrentView}
            darkMode={darkMode}
            onToggleDarkMode={toggleDarkMode}
          />
          
          {/* Main Content Area */}
          <main className="flex-1 flex flex-col overflow-hidden">
            {renderCurrentView()}
          </main>
        </div>
      </div>
    </ErrorBoundary>
  );
}

export default App;
