import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Hide React error overlay for MetaMask errors
const hideMetaMaskOverlay = () => {
  const overlay = document.getElementById('webpack-dev-server-client-overlay');
  if (overlay && overlay.innerHTML?.includes('MetaMask')) {
    overlay.style.display = 'none';
  }
  // Also check for iframe overlay
  const iframes = document.querySelectorAll('iframe');
  iframes.forEach(iframe => {
    if (iframe.id?.includes('overlay') || iframe.src?.includes('overlay')) {
      try {
        const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
        if (iframeDoc?.body?.innerHTML?.includes('MetaMask')) {
          iframe.style.display = 'none';
        }
      } catch (e) {}
    }
  });
};

// Run periodically to catch the overlay
setInterval(hideMetaMaskOverlay, 100);

// Also observe DOM for overlay additions
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.addedNodes.forEach((node) => {
      if (node.nodeType === 1) {
        if (node.id?.includes('overlay') || node.innerHTML?.includes('MetaMask')) {
          node.style.display = 'none';
        }
      }
    });
  });
});
observer.observe(document.body || document.documentElement, { childList: true, subtree: true });

// Suppress MetaMask and other wallet extension errors completely
const originalError = console.error;
console.error = (...args) => {
  const errorString = args.map(a => a?.toString?.() || '').join(' ');
  if (errorString.includes('MetaMask') || 
      errorString.includes('ethereum') ||
      errorString.includes('inpage.js') ||
      errorString.includes('Failed to connect') ||
      args[0]?.message?.includes('MetaMask')) {
    return;
  }
  originalError.apply(console, args);
};

// Override window.onerror to catch extension errors
window.onerror = function(message, source, lineno, colno, error) {
  if (message?.includes('MetaMask') || 
      source?.includes('inpage.js') ||
      source?.includes('chrome-extension') ||
      message?.includes('Failed to connect')) {
    return true; // Prevents the error from showing
  }
  return false;
};

// Suppress uncaught errors from browser extensions
window.addEventListener('error', (event) => {
  if (event.message?.includes('MetaMask') || 
      event.message?.includes('Failed to connect') ||
      event.filename?.includes('inpage.js') ||
      event.filename?.includes('chrome-extension')) {
    event.preventDefault();
    event.stopPropagation();
    return true;
  }
}, true);

window.addEventListener('unhandledrejection', (event) => {
  if (event.reason?.message?.includes('MetaMask') ||
      event.reason?.message?.includes('Failed to connect') ||
      event.reason?.toString?.().includes('MetaMask')) {
    event.preventDefault();
    event.stopPropagation();
    return true;
  }
}, true);

// Create root element
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the app
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
