import React, { useState, useEffect, useRef } from 'react';

const BadgesLegend: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const legendRef = useRef<HTMLDivElement>(null);

  // Close the legend when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (legendRef.current && !legendRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }

    // Add event listener when legend is open
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    
    // Cleanup
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  return (
    <div className="relative inline-block" ref={legendRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="text-sm text-blue-600 hover:text-blue-800 flex items-center ml-2"
        aria-label="Show badge meanings"
        aria-expanded={isOpen}
      >
        <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        What do these badges mean?
      </button>

      {isOpen && (
        <div 
          className="absolute z-10 mt-2 right-0 bg-white rounded-md shadow-lg p-4 w-72 border border-gray-200"
          role="tooltip"
          aria-hidden={!isOpen}
        >
          <div className="flex justify-between items-start mb-2">
            <h3 className="font-medium text-gray-800">Article Analysis Badges</h3>
            <button 
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-gray-600"
              aria-label="Close legend"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-700 mb-1">Sentiment:</h4>
              <div className="flex flex-wrap gap-2 mb-1">
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 flex items-center">
                  <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                  </svg>
                  positive
                </span>
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 flex items-center">
                  <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd"></path>
                  </svg>
                  neutral
                </span>
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 flex items-center">
                  <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"></path>
                  </svg>
                  negative
                </span>
              </div>
              <p className="text-xs text-gray-600">Indicates the emotional tone of the article. Positive articles use supportive language, negative ones use critical language, and neutral articles maintain a balanced tone.</p>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-700 mb-1">Political Perspective:</h4>
              <div className="flex flex-wrap gap-2 mb-1">
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">left-leaning</span>
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">centrist</span>
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">right-leaning</span>
              </div>
              <p className="text-xs text-gray-600">Shows the political orientation detected in the content. This helps identify potential political bias in the reporting and provides context for the viewpoint presented.</p>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-700 mb-1">Factual Reporting:</h4>
              <div className="flex flex-wrap gap-2 mb-1">
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">factual</span>
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">somewhat sensational</span>
                <span className="px-2 py-1 rounded-full text-xs font-medium bg-orange-100 text-orange-800">highly sensational</span>
              </div>
              <p className="text-xs text-gray-600">Measures how fact-based versus emotionally charged or exaggerated the reporting is. Factual articles focus on verifiable information, while sensational ones use dramatic language to evoke emotional responses.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BadgesLegend;