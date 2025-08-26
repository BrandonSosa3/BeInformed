import React from 'react';
import TopicStatsCard from './TopicStatsCard';

export interface TopicStatsData {
  totalArticles: number;
  analyzedArticles: number;
  averageSentiment: number;
  sentimentDistribution: {
    positive: number;
    neutral: number;
    negative: number;
  };
  biasDistribution: {
    leftLeaning: number;
    centrist: number;
    rightLeaning: number;
  };
  sourcesCount: number;
  sensationalismLevel: number;
  timeRange: string;
}

interface TopicStatisticsProps {
  stats: TopicStatsData;
  isLoading?: boolean;
}

const TopicStatistics: React.FC<TopicStatisticsProps> = ({ 
  stats, 
  isLoading = false 
}) => {
  // Create a default stats object to use if stats is invalid
  const defaultStats: TopicStatsData = {
    totalArticles: 0,
    analyzedArticles: 0,
    averageSentiment: 0,
    sentimentDistribution: { positive: 0, neutral: 0, negative: 0 },
    biasDistribution: { leftLeaning: 0, centrist: 0, rightLeaning: 0 },
    sourcesCount: 0,
    sensationalismLevel: 0,
    timeRange: "all time"
  };

  // Safely access stats or use defaults
  const safeStats = stats && typeof stats === 'object' ? stats : defaultStats;
  
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 animate-pulse">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-gray-100 rounded-lg h-24"></div>
        ))}
      </div>
    );
  }
  
  // Calculate percentage of articles analyzed (safely)
  const analysisPercentage = 
    safeStats.totalArticles > 0 
      ? Math.round((safeStats.analyzedArticles / safeStats.totalArticles) * 100) 
      : 0;
  
  // Determine overall sentiment label
  const getSentimentLabel = (score: number): string => {
    if (score === undefined || isNaN(score) || safeStats.analyzedArticles === 0) return "Unknown";
    if (score > 0.3) return 'Mostly Positive';
    if (score < -0.3) return 'Mostly Negative';
    return 'Neutral';
  };
  
  // Determine overall bias label
  const getBiasLabel = (): string => {
    const { leftLeaning, centrist, rightLeaning } = safeStats.biasDistribution || { leftLeaning: 0, centrist: 0, rightLeaning: 0 };
    const total = (leftLeaning || 0) + (centrist || 0) + (rightLeaning || 0);
    
    if (total === 0 || safeStats.analyzedArticles === 0) return 'Unknown';
    
    const leftPercent = (leftLeaning / total) * 100;
    const rightPercent = (rightLeaning / total) * 100;
    const centristPercent = (centrist / total) * 100;
    
    if (centristPercent > 60) return 'Mostly Centrist';
    if (leftPercent > rightPercent + 20) return 'Left-Leaning';
    if (rightPercent > leftPercent + 20) return 'Right-Leaning';
    return 'Mixed Perspectives';
  };

  // Determine if we have valid data
  const hasValidData = safeStats.analyzedArticles > 0;
  
  return (
    <div className="mb-8">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Topic Overview</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Articles Card */}
        <TopicStatsCard
          title="Articles Found"
          value={safeStats.totalArticles || 0}
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
            </svg>
          }
          color="blue"
        />
        
        {/* Analysis Coverage Card */}
        <TopicStatsCard
          title="Analysis Coverage"
          value={`${analysisPercentage}%`}
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          }
          color="purple"
        />
        
        {/* Overall Sentiment Card */}
        <TopicStatsCard
          title="Overall Sentiment"
          value={getSentimentLabel(safeStats.averageSentiment)}
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          }
          color={hasValidData ? (safeStats.averageSentiment > 0 ? "green" : safeStats.averageSentiment < 0 ? "red" : "gray") : "gray"}
          change={hasValidData ? Math.round((safeStats.averageSentiment || 0) * 100) : undefined}
          changeLabel={hasValidData ? "sentiment score" : undefined}
        />
        
        {/* Political Perspective Card */}
        <TopicStatsCard
          title="Political Perspective"
          value={getBiasLabel()}
          icon={
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
            </svg>
          }
          color={getBiasLabel().includes('Left') ? "blue" : getBiasLabel().includes('Right') ? "red" : "yellow"}
        />
      </div>
      
      <div className="text-xs text-gray-500 mt-2 text-right">
        Analysis based on {safeStats.analyzedArticles || 0} of {safeStats.totalArticles || 0} articles from {safeStats.timeRange || "all time"}
      </div>
    </div>
  );
};

export default TopicStatistics;