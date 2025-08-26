import React from 'react';
import { useBackendHealth } from '../hooks/useBackendHealth';

interface BackendStatusBannerProps {
  onRetry?: () => void;
}

export const BackendStatusBanner: React.FC<BackendStatusBannerProps> = ({ onRetry }) => {
  const { isHealthy, isChecking, isSpinningUp, message, retryHealthCheck } = useBackendHealth();

  // Don't show banner if backend is healthy
  if (isHealthy) return null;

  return (
    <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 shadow-lg">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {isChecking && (
            <div className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
              <span className="font-medium">Backend Status</span>
            </div>
          )}
          
          <div className="flex flex-col">
            <p className="text-sm font-medium">{message}</p>
            {isSpinningUp && (
              <p className="text-xs opacity-90 mt-1">
                The backend is hosted on Render's free tier and needs to spin up after periods of inactivity.
                Search functionality will be available once ready.
              </p>
            )}
          </div>
        </div>

        {!isChecking && (
          <button
            onClick={() => {
              retryHealthCheck();
              onRetry?.();
            }}
            className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            Retry
          </button>
        )}
      </div>
    </div>
  );
};

// Search disabled overlay component
interface SearchOverlayProps {
  isBackendReady: boolean;
  children: React.ReactNode;
}

export const SearchOverlay: React.FC<SearchOverlayProps> = ({ isBackendReady, children }) => {
  if (isBackendReady) {
    return <>{children}</>;
  }

  return (
    <div className="relative">
      {children}
      <div className="absolute inset-0 bg-gray-100/80 backdrop-blur-sm rounded-lg flex items-center justify-center z-10">
        <div className="text-center p-4">
          <div className="animate-spin rounded-full h-8 w-8 border-2 border-blue-500 border-t-transparent mx-auto mb-3"></div>
          <p className="text-gray-600 font-medium">Waiting for backend...</p>
          <p className="text-sm text-gray-500 mt-1">Search will be enabled once ready</p>
        </div>
      </div>
    </div>
  );
};