import React from 'react';
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary';
import { ErrorFallback } from './components/ErrorHandling/ErrorFallback';
import AppRouter from "./routes/AppRouter";

// Global error handler
const handleGlobalError = (error, errorInfo) => {
  console.error('Global error caught:', error, errorInfo);
  
  // Log error to monitoring service if available
  if (window.errorTracker) {
    window.errorTracker.captureException(error, {
      context: 'App',
      errorInfo: errorInfo?.componentStack
    });
  }
};

function App() {
    return (
        <ErrorBoundary 
            fallback={ErrorFallback}
            onError={handleGlobalError}
        >
            <div className="app">
                <AppRouter />
            </div>
        </ErrorBoundary>
    );
}

export default App;