import React from 'react';

interface SourceStats {
  sourceId: number | null;
  sourceName: string;
  articleCount: number;
  averageSentiment: number;
  averageBias: number;
  averageSensationalism: number;
}

interface SourceCredibilityRankingProps {
  sources: SourceStats[];
  isLoading?: boolean;
  maxDisplay?: number;
  title?: string;
}

const SourceCredibilityRanking: React.FC<SourceCredibilityRankingProps> = ({
  sources,
  isLoading = false,
  maxDisplay = 5,
  title = 'Source Credibility Ranking'
}) => {
  // Calculate credibility score - lower sensationalism = higher credibility
  const sourcesWithScore = sources.map(source => ({
    ...source,
    credibilityScore: Math.round((1 - source.averageSensationalism) * 100) // Convert to 0-100 scale
  }));
  
  // Sort by credibility score (descending)
  const sortedSources = [...sourcesWithScore].sort((a, b) => 
    b.credibilityScore - a.credibilityScore
  );
  
  // Limit to maxDisplay
  const displaySources = sortedSources.slice(0, maxDisplay);

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-4 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="space-y-3">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="flex items-center">
              <div className="h-4 bg-gray-200 rounded w-1/4 mr-2"></div>
              <div className="h-4 bg-gray-100 rounded w-3/4"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // If no sources
  if (!sources.length) {
    return (
      <div className="bg-white rounded-lg shadow p-4">
        <h3 className="text-lg font-medium text-gray-700 mb-4">{title}</h3>
        <div className="text-center py-6 text-gray-500">
          No source data available
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <h3 className="text-lg font-medium text-gray-700 mb-4">{title}</h3>
      
      <div className="space-y-4">
        {displaySources.map((source, index) => (
          <div key={source.sourceId || index} className="border-b border-gray-100 pb-3 last:border-b-0 last:pb-0">
            <div className="flex justify-between items-center mb-1">
              <div className="font-medium text-gray-800">
                {index + 1}. {source.sourceName}
              </div>
              <div className="text-sm text-gray-500">
                {source.articleCount} article{source.articleCount !== 1 ? 's' : ''}
              </div>
            </div>
            
            {/* Credibility score bar */}
            <div className="w-full bg-gray-100 rounded-full h-2.5 mb-1">
              <div 
                className={`h-2.5 rounded-full ${
                  source.credibilityScore > 70 ? 'bg-green-500' :
                  source.credibilityScore > 50 ? 'bg-yellow-500' : 'bg-orange-500'
                }`}
                style={{ width: `${source.credibilityScore}%` }}
              ></div>
            </div>
            
            <div className="flex justify-between text-xs text-gray-500">
              <span>Credibility score: {source.credibilityScore}</span>
              <span>Bias: {getBiasLabel(source.averageBias)}</span>
            </div>
          </div>
        ))}
      </div>
      
      {sources.length > maxDisplay && (
        <div className="mt-3 text-center">
          <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
            View all {sources.length} sources
          </button>
        </div>
      )}
    </div>
  );
};

// Helper function to get bias label from score
const getBiasLabel = (score: number): string => {
  if (score < -0.3) return 'Left-leaning';
  if (score > 0.3) return 'Right-leaning';
  return 'Center';
};

export default SourceCredibilityRanking;