import React, { useState } from 'react';
import Navigation from './navigation/Navigation';
import ProblemSolverView from './views/ProblemSolverView';
import ConceptExplainerView from './views/ConceptExplainerView';
import FormulaReferenceView from './views/FormulaReferenceView';
import StudyTipsView from './views/StudyTipsView';
import ImageGenerator from './components/ImageGenerator';
import VoiceView from './views/VoiceView';
import ErrorBoundary from './components/ErrorBoundary';
import './index.css';

function App() {
  const [currentView, setCurrentView] = useState('solver');

  const renderCurrentView = () => {
    switch (currentView) {
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
        return <ProblemSolverView />;
    }
  };

  return (
    <ErrorBoundary>
      <div className="h-screen overflow-hidden bg-gradient-to-br from-blue-50 via-indigo-50 to-blue-100">
        <div className="flex h-full">
          {/* Fixed Sidebar */}
          <Navigation 
            currentView={currentView} 
            onViewChange={setCurrentView}
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
