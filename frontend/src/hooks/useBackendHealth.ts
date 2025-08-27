// hooks/useBackendHealth.ts
import { useState, useEffect, useRef } from 'react';
import { API_URL } from '../services/api';

interface HealthStatus {
  isHealthy: boolean;
  isChecking: boolean;
  isSpinningUp: boolean;
  retryCount: number;
  message: string;
}

export const useBackendHealth = () => {
  const [status, setStatus] = useState<HealthStatus>({
    isHealthy: false,
    isChecking: true,
    isSpinningUp: false,
    retryCount: 0,
    message: 'Checking backend status...'
  });

  const intervalRef = useRef<number | null>(null);
  const maxRetries = 40; // 40 * 5 seconds = 200 seconds (3.3 minutes)

  const checkHealth = async (): Promise<boolean> => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);
  
      // Use the sources endpoint which already works with CORS
      const response = await fetch(`${API_URL}/sources?limit=1`, {
        signal: controller.signal,
        headers: {
          'Cache-Control': 'no-cache'
        }
      });
  
      clearTimeout(timeoutId);
      return response.ok;
    } catch (error) {
      return false;
    }
  };

  const startHealthCheck = () => {
    setStatus(prev => ({ ...prev, isChecking: true }));

    const performCheck = async () => {
      const isHealthy = await checkHealth();
      
      setStatus(prev => {
        const newRetryCount = prev.retryCount + 1;
        
        if (isHealthy) {
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
          }
          return {
            isHealthy: true,
            isChecking: false,
            isSpinningUp: false,
            retryCount: newRetryCount,
            message: 'Backend is ready!'
          };
        }

        // Determine if backend is spinning up
        const isSpinningUp = newRetryCount > 2 && newRetryCount < maxRetries;
        
        let message = 'Checking backend status...';
        if (isSpinningUp) {
          const estimatedMinutes = Math.ceil((maxRetries - newRetryCount) * 5 / 60);
          message = `Backend is starting up... Estimated wait: ${estimatedMinutes} minute(s)`;
        } else if (newRetryCount >= maxRetries) {
          message = 'Backend appears to be unavailable. Please try again later.';
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
          }
        }

        return {
          isHealthy: false,
          isChecking: newRetryCount < maxRetries,
          isSpinningUp,
          retryCount: newRetryCount,
          message
        };
      });
    };

    // Initial check
    performCheck();

    // Set up interval for subsequent checks
    intervalRef.current = setInterval(performCheck, 5000); // Check every 5 seconds
  };

    // In useBackendHealth.ts, replace the useEffect with:
    useEffect(() => {
        // Only show loading state in production
        const isProduction = !window.location.hostname.includes('localhost') && !window.location.hostname.includes('127.0.0.1');
        
        if (!isProduction) {
        // Local development - immediately ready
        setStatus({
            isHealthy: true,
            isChecking: false,
            isSpinningUp: false,
            retryCount: 0,
            message: 'Ready'
        });
        return;
        }
    
        // Production - show loading for 3 minutes, then assume ready
        setStatus({
        isHealthy: false,
        isChecking: true,
        isSpinningUp: true,
        retryCount: 0,
        message: 'Backend is starting up... Estimated wait: 1 min 30 seconds maximum as I am hosting backend on free render plan which spins down with inactivity!'
        });
    
        // After 3 minutes, assume backend is ready
        const timer = setTimeout(() => {
        setStatus({
            isHealthy: true,
            isChecking: false,
            isSpinningUp: false,
            retryCount: 0,
            message: 'Backend should be ready now'
        });
        }, 65000); // 3 minutes
    
        return () => clearTimeout(timer);
    }, []);

  const retryHealthCheck = () => {
    setStatus({
      isHealthy: false,
      isChecking: true,
      isSpinningUp: false,
      retryCount: 0,
      message: 'Checking backend status...'
    });
    startHealthCheck();
  };

  return {
    ...status,
    retryHealthCheck
  };
};
