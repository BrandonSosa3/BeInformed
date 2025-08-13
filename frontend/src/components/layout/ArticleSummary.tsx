import React from 'react';
import type { Article } from '../../types/api';

interface ArticleSummaryProps {
  article: Article;
}

const ArticleSummary: React.FC<ArticleSummaryProps> = ({ article }) => {
  // Check if article has a beginner summary
  if (!article.beginner_summary) {
    return null;
  }
  
  return (
    <div className="bg-blue-50 border-l-4 border-blue-500 rounded-lg shadow-md p-5 mb-6">
      <div className="flex items-center mb-3">
        <svg className="w-5 h-5 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h3 className="text-lg font-semibold text-blue-800">AI Generated Quick Summary</h3>
      </div>
      
      {/* Summary content */}
      <div className="text-gray-700">
        <p>{article.beginner_summary}</p>
      </div>
    </div>
  );
};

export default ArticleSummary;