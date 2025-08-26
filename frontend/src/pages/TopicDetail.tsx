import React, { useState, useEffect } from 'react';
import { useMemo } from 'react';
import { useParams, Link } from 'react-router-dom';
import { topicApi } from '../services/api';
import type { Topic, ArticleList, TopicStatsData, SourceStats } from '../types/api';
import TopicStatistics from '../components/dashboard/TopicStatistics';
import ArticleFilters from '../components/dashboard/ArticleFilters';
import BadgesLegend from '../components/BadgesLegend';

interface SentimentTimeData {
    dates: string[];
    sentiment: number[];
    counts: number[];
  }

const TopicDetail: React.FC = () => {
  const { topicId } = useParams<{ topicId: string }>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [topic, setTopic] = useState<Topic | null>(null);
  const [articleList, setArticleList] = useState<ArticleList | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [stats, setStats] = useState<TopicStatsData | null>(null);
  const [statsLoading, setStatsLoading] = useState(true);

  const [sentimentTrends, setSentimentTrends] = useState<SentimentTimeData>({ 
    dates: [], 
    sentiment: [], 
    counts: [] 
  });
  const [sentimentTrendsLoading, setSentimentTrendsLoading] = useState(true);

  const [sourceStats, setSourceStats] = useState<SourceStats[]>([]);
  const [sourceStatsLoading, setSourceStatsLoading] = useState(true);

  const [filters, setFilters] = useState<{
    sentiment: string[];
    bias: string[];
    sources: string[];
    dateRange: string;
  }>({
    sentiment: [],
    bias: [],
    sources: [],
    dateRange: 'all'
  });
  
  const fetchTopic = async () => {
    setLoading(true);
    setError(null);
    
    try {
      if (!topicId) {
        throw new Error('Topic ID is required');
      }
      
      // Get topic details
      const topicData = await topicApi.getTopic(parseInt(topicId));
      setTopic(topicData);
      
      // Get topic articles
      const articles = await topicApi.getTopicArticles(parseInt(topicId), {
        page: currentPage,
        size: 10
      });
      setArticleList(articles);
    } catch (err) {
      console.error('Error fetching topic:', err);
      setError('Failed to load topic data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Get available sources from articles
  const availableSources = useMemo(() => {
    if (!articleList || !articleList.items) return [];
    
    const sources = articleList.items
      .map(article => article.source_name)
      .filter((name): name is string => Boolean(name)); // Type guard to ensure non-null strings
    
    return Array.from(new Set(sources)).sort();
  }, [articleList]);
  
  // Add a function to filter articles
  const filteredArticles = useMemo(() => {
    if (!articleList || !articleList.items) return [];
    
    return articleList.items.filter(article => {
      // Filter by sentiment
      if (filters.sentiment.length > 0 && article.sentiment_label) {
        if (!filters.sentiment.includes(article.sentiment_label)) {
          return false;
        }
      }
      
      // Filter by bias
      if (filters.bias.length > 0 && article.political_bias_label) {
        if (!filters.bias.includes(article.political_bias_label)) {
          return false;
        }
      }
      
      // Filter by source
      if (filters.sources.length > 0 && article.source_name) {
        if (!filters.sources.includes(article.source_name)) {
          return false;
        }
      }
      
      // Filter by date range
      if (filters.dateRange !== 'all' && article.published_at) {
        const publishDate = new Date(article.published_at);
        const now = new Date();
        const daysAgo = parseInt(filters.dateRange);
        const cutoffDate = new Date(now.setDate(now.getDate() - daysAgo));
        
        if (publishDate < cutoffDate) {
          return false;
        }
      }
      
      return true;
    });
  }, [articleList, filters]);
  
  // Handle filter changes
  const handleFilterChange = (newFilters: {
    sentiment: string[];
    bias: string[];
    sources: string[];
    dateRange: string;
  }) => {
    setFilters(newFilters);
  };
  
  // Fetch topic data and articles
  useEffect(() => {
    fetchTopic();
  }, [topicId, currentPage]);
  
  // Fetch topic statistics
  useEffect(() => {
    const fetchStatistics = async () => {
      if (!topicId) return;
      
      setStatsLoading(true);
      try {
        console.log("Fetching statistics for topic:", topicId);
        if (topicApi.getTopicStatistics) {
          const statsData = await topicApi.getTopicStatistics(parseInt(topicId), 30);
          console.log("Received statistics data:", statsData);
          setStats(statsData);
        } else {
          console.error("topicApi.getTopicStatistics function not available");
        }
      } catch (err) {
        console.error('Error fetching topic statistics:', err);
      } finally {
        setStatsLoading(false);
      }
    };
    
    fetchStatistics();
  }, [topicId]);

  useEffect(() => {
    const fetchSentimentTrends = async () => {
      if (!topicId) return;
      
      setSentimentTrendsLoading(true);
      try {
        if (topicApi.getSentimentOverTime) {
          const trendsData = await topicApi.getSentimentOverTime(parseInt(topicId), 30, 'day');
          setSentimentTrends(trendsData);
        }
      } catch (err) {
        console.error('Error fetching sentiment trends:', err);
        // Don't set error state, as this is secondary data
      } finally {
        setSentimentTrendsLoading(false);
      }
    };
    
    fetchSentimentTrends();
  }, [topicId]);

  useEffect(() => {
    const fetchSourceStats = async () => {
      if (!topicId) return;
      
      setSourceStatsLoading(true);
      try {
        if (topicApi.getTopicSourceStatistics) {
          const sources = await topicApi.getTopicSourceStatistics(parseInt(topicId));
          setSourceStats(sources);
        }
      } catch (err) {
        console.error('Error fetching source statistics:', err);
        // Don't set error state, as this is secondary data
      } finally {
        setSourceStatsLoading(false);
      }
    };
    
    fetchSourceStats();
  }, [topicId]);

    // Create a function to refresh all data at once
    const refreshData = () => {
        fetchTopic();
        
        if (topicApi.getTopicStatistics && topicId) {
          topicApi.getTopicStatistics(parseInt(topicId), 30).then(setStats);
        }
        
        if (topicApi.getSentimentOverTime && topicId) {
          topicApi.getSentimentOverTime(parseInt(topicId), 30, 'day').then(setSentimentTrends);
        }
        
        if (topicApi.getTopicSourceStatistics && topicId) {
          topicApi.getTopicSourceStatistics(parseInt(topicId)).then(setSourceStats);
        }
      };

  
  const handlePageChange = (page: number) => {
    if (page >= 1 && (!articleList || page <= articleList.pages)) {
      setCurrentPage(page);
    }
  };
  
  const handleAnalyzeTopic = async () => {
    if (!topicId) return;
    
    setIsAnalyzing(true);
    
    try {
      console.log("Starting topic analysis for topic:", topicId);
      
      // Call the analysis API
      const response = await fetch(`http://localhost:8000/api/v1/analysis/topics/${topicId}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const analysisResult = await response.json();
      console.log("Analysis completed with result:", analysisResult);
      
      // Wait to ensure backend processing completes
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      // Refresh the data
      await fetchTopic();
      
      // Explicitly fetch fresh statistics
      if (topicApi.getTopicStatistics) {
        console.log("Fetching fresh statistics after analysis");
        const statsData = await topicApi.getTopicStatistics(parseInt(topicId), 30);
        console.log("Fresh statistics after analysis:", statsData);
        setStats(statsData);
      }
    } catch (error) {
      console.error('Error analyzing topic:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };
  
  const handleAnalyzeArticle = async (articleId: number) => {
    try {
      // Call the analysis API
      const response = await fetch(`http://localhost:8000/api/v1/analysis/articles/${articleId}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error('Failed to analyze article');
      }
      
      // Refresh the data
      await fetchTopic();
      
      // Refresh statistics after analysis
      if (topicApi.getTopicStatistics) {
        setTimeout(async () => {
          const statsData = await topicApi.getTopicStatistics(parseInt(topicId!), 30);
          setStats(statsData);
        }, 1000);
      }
    } catch (error) {
      console.error('Error analyzing article:', error);
    }
  };
  
  // Helper function to get bias analysis stats for topic
  const getBiasStats = () => {
    if (!articleList || !articleList.items.length) return null;
    
    const analyzed = articleList.items.filter(article => article.last_analyzed_at);
    if (!analyzed.length) return null;
    
    const leftLeaning = analyzed.filter(article => article.political_bias_label === 'left-leaning').length;
    const rightLeaning = analyzed.filter(article => article.political_bias_label === 'right-leaning').length;
    const centrist = analyzed.filter(article => 
      article.political_bias_label === 'centrist' || article.political_bias_label === 'neutral'
    ).length;
    
    const factual = analyzed.filter(article => article.sensationalism_label === 'factual').length;
    const somewhatSensational = analyzed.filter(article => article.sensationalism_label === 'somewhat sensational').length;
    const highlySensational = analyzed.filter(article => article.sensationalism_label === 'highly sensational').length;
    
    return {
      analyzed: analyzed.length,
      political: { leftLeaning, rightLeaning, centrist },
      sensationalism: { factual, somewhatSensational, highlySensational }
    };
  };
  
  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8 flex justify-center">
        <svg className="animate-spin h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    );
  }
  
  if (error || !topic || !articleList) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
          <p className="font-bold">Error</p>
          <p>{error || 'Failed to load topic data.'}</p>
        </div>
        <Link to="/search" className="text-blue-600 hover:text-blue-800">
          &larr; Back to Search
        </Link>
      </div>
    );
  }
  
  // Calculate bias stats
  const biasStats = getBiasStats();

  // Create a better local stats object directly from the articles
  const localStats = articleList ? {
    totalArticles: articleList.total,
    analyzedArticles: articleList.items.filter(article => article.last_analyzed_at).length,
    averageSentiment: 0, // Can't easily calculate this
    sentimentDistribution: {
      positive: articleList.items.filter(a => a.sentiment_label === 'positive').length,
      neutral: articleList.items.filter(a => a.sentiment_label === 'neutral').length,
      negative: articleList.items.filter(a => a.sentiment_label === 'negative').length
    },
    biasDistribution: {
      leftLeaning: articleList.items.filter(a => a.political_bias_label === 'left-leaning').length,
      centrist: articleList.items.filter(a => a.political_bias_label === 'centrist' || a.political_bias_label === 'neutral').length,
      rightLeaning: articleList.items.filter(a => a.political_bias_label === 'right-leaning').length
    },
    sourcesCount: new Set(articleList.items.map(a => a.source_name).filter(Boolean)).size,
    sensationalismLevel: 0, // Can't easily calculate this
    timeRange: "current page"
  } : null;
  
  // Use API stats if they look valid, otherwise use our local calculation
  const displayStats = (stats && stats.totalArticles > 0) ? stats : localStats;

  
  
  return (
    <div className="container mx-auto px-4 py-8">
      {/* Back link */}
      <Link to="/search" className="text-blue-600 hover:text-blue-800 mb-6 inline-block">
        &larr; Back to Search
      </Link>
      
      {/* Topic header */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{topic.name}</h1>
        <div className="flex flex-wrap gap-4 mt-2 text-sm text-gray-600">
          <div>Searched {topic.search_count} times</div>
          <div>Last searched: {topic.last_searched_at ? new Date(topic.last_searched_at).toLocaleString() : 'Never'}</div>
          <div>{articleList.total} articles found</div>
        </div>
        
        {/* Add Analyze and Refresh buttons */}
        <div className="mt-4 flex">
          <button
            onClick={() => handleAnalyzeTopic()}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium px-4 py-2 rounded-md transition-colors mr-2 flex items-center"
            disabled={isAnalyzing}
          >
            {isAnalyzing ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </>
            ) : (
              <>
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
                Analyze Articles
              </>
            )}
          </button>
          <button
            onClick={refreshData}
            className="bg-gray-100 hover:bg-gray-200 text-gray-800 font-medium px-4 py-2 rounded-md transition-colors flex items-center"
            >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            Refresh
          </button>
        </div>
      </div>
      
      {/* Use the new TopicStatistics component if available */}
      {displayStats && (
        <TopicStatistics stats={displayStats} isLoading={statsLoading} />
      )}
      
      {/* Keep the existing Bias Analysis Summary if new stats not available */}
      {!stats && biasStats && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Topic Analysis</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Political Bias Distribution */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-medium text-gray-700 mb-3">Political Perspective</h3>
              
              {/* Political bias bar chart */}
              <div className="flex items-end h-28 mb-2">
                <div className="w-1/3 px-1">
                  <div 
                    className="bg-blue-500 w-full relative rounded-t"
                    style={{ 
                      height: `${biasStats.political.leftLeaning / biasStats.analyzed * 100}%`,
                      minHeight: biasStats.political.leftLeaning ? '8px' : '0'
                    }}
                  >
                    {biasStats.political.leftLeaning > 0 && (
                      <span className="absolute -top-6 left-0 right-0 text-center text-sm font-medium">
                        {biasStats.political.leftLeaning}
                      </span>
                    )}
                  </div>
                </div>
                <div className="w-1/3 px-1">
                  <div 
                    className="bg-purple-500 w-full relative rounded-t"
                    style={{ 
                      height: `${biasStats.political.centrist / biasStats.analyzed * 100}%`,
                      minHeight: biasStats.political.centrist ? '8px' : '0'
                    }}
                  >
                    {biasStats.political.centrist > 0 && (
                      <span className="absolute -top-6 left-0 right-0 text-center text-sm font-medium">
                        {biasStats.political.centrist}
                      </span>
                    )}
                  </div>
                </div>
                <div className="w-1/3 px-1">
                  <div 
                    className="bg-red-500 w-full relative rounded-t"
                    style={{ 
                      height: `${biasStats.political.rightLeaning / biasStats.analyzed * 100}%`,
                      minHeight: biasStats.political.rightLeaning ? '8px' : '0'
                    }}
                  >
                    {biasStats.political.rightLeaning > 0 && (
                      <span className="absolute -top-6 left-0 right-0 text-center text-sm font-medium">
                        {biasStats.political.rightLeaning}
                      </span>
                    )}
                  </div>
                </div>
              </div>
              
              {/* Labels */}
              <div className="flex text-xs text-gray-600 justify-between">
                <div className="text-center w-1/3">Left-leaning</div>
                <div className="text-center w-1/3">Centrist</div>
                <div className="text-center w-1/3">Right-leaning</div>
              </div>
            </div>
            
            {/* Sensationalism Distribution */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-medium text-gray-700 mb-3">Sensationalism Level</h3>
              
              {/* Sensationalism bar chart */}
              <div className="flex items-end h-28 mb-2">
                <div className="w-1/3 px-1">
                  <div 
                    className="bg-green-500 w-full relative rounded-t"
                    style={{ 
                      height: `${biasStats.sensationalism.factual / biasStats.analyzed * 100}%`,
                      minHeight: biasStats.sensationalism.factual ? '8px' : '0'
                    }}
                  >
                    {biasStats.sensationalism.factual > 0 && (
                      <span className="absolute -top-6 left-0 right-0 text-center text-sm font-medium">
                        {biasStats.sensationalism.factual}
                      </span>
                    )}
                  </div>
                </div>
                <div className="w-1/3 px-1">
                  <div 
                    className="bg-yellow-500 w-full relative rounded-t"
                    style={{ 
                      height: `${biasStats.sensationalism.somewhatSensational / biasStats.analyzed * 100}%`,
                      minHeight: biasStats.sensationalism.somewhatSensational ? '8px' : '0'
                    }}
                  >
                    {biasStats.sensationalism.somewhatSensational > 0 && (
                      <span className="absolute -top-6 left-0 right-0 text-center text-sm font-medium">
                        {biasStats.sensationalism.somewhatSensational}
                      </span>
                    )}
                  </div>
                </div>
                <div className="w-1/3 px-1">
                  <div 
                    className="bg-orange-500 w-full relative rounded-t"
                    style={{ 
                      height: `${biasStats.sensationalism.highlySensational / biasStats.analyzed * 100}%`,
                      minHeight: biasStats.sensationalism.highlySensational ? '8px' : '0'
                    }}
                  >
                    {biasStats.sensationalism.highlySensational > 0 && (
                      <span className="absolute -top-6 left-0 right-0 text-center text-sm font-medium">
                        {biasStats.sensationalism.highlySensational}
                      </span>
                    )}
                  </div>
                </div>
              </div>
              
              {/* Labels */}
              <div className="flex text-xs text-gray-600 justify-between">
                <div className="text-center w-1/3">Factual</div>
                <div className="text-center w-1/3">Somewhat<br/>Sensational</div>
                <div className="text-center w-1/3">Highly<br/>Sensational</div>
              </div>
            </div>
          </div>
          
          <div className="mt-4 text-sm text-gray-500">
            Based on analysis of {biasStats.analyzed} out of {articleList.total} articles
          </div>
        </div>
      )}

      {/* Article Filters */}
      <ArticleFilters 
        onFilterChange={handleFilterChange}
        availableSources={availableSources}
        initialFilters={filters}
      />

      {/* Articles list */}
      <div className="bg-white rounded-lg shadow overflow-hidden mb-6">
        <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
          <div className="flex items-center">
            <h2 className="text-xl font-semibold text-gray-800">Articles</h2>
            <BadgesLegend />
          </div>
          {filteredArticles.length !== articleList.items.length && (
            <span className="text-sm text-gray-500">
              Showing {filteredArticles.length} of {articleList.total} articles
            </span>
          )}
        </div>
        
        <div className="divide-y divide-gray-200">
          {filteredArticles.length > 0 ? (
            filteredArticles.map((article) => (
              <div key={article.id} className="p-6 border-b border-gray-200 last:border-b-0">
                <div className="flex justify-between items-start">
                  <h3 className="text-lg font-medium text-gray-900 flex-grow">
                    <Link 
                      to={`/articles/${article.id}`}
                      className="hover:text-blue-600"
                    >
                      {article.title}
                    </Link>
                  </h3>
                  
                  {/* Analysis badges container */}
                  <div className="flex flex-wrap gap-2 ml-2 mt-1">
                    {/* Sentiment badge */}
                    {article.sentiment_label && (
                      <span 
                        className={`px-2 py-1 rounded-full text-xs font-medium flex items-center ${
                          article.sentiment_label === 'positive' 
                            ? 'bg-green-100 text-green-800' 
                            : article.sentiment_label === 'negative'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {article.sentiment_label === 'positive' && (
                          <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                          </svg>
                        )}
                        {article.sentiment_label === 'negative' && (
                          <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"></path>
                          </svg>
                        )}
                        {article.sentiment_label === 'neutral' && (
                          <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd"></path>
                          </svg>
                        )}
                        {article.sentiment_label}
                      </span>
                    )}
                    
                    {/* Political bias badge */}
                    {article.political_bias_label && (
                      <span 
                        className={`px-2 py-1 rounded-full text-xs font-medium flex items-center ${
                          article.political_bias_label === 'left-leaning' 
                            ? 'bg-blue-100 text-blue-800' 
                            : article.political_bias_label === 'right-leaning'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-purple-100 text-purple-800'
                        }`}
                      >
                        {article.political_bias_label}
                      </span>
                    )}
                    
                    {/* Sensationalism badge */}
                    {article.sensationalism_label && (
                      <span 
                        className={`px-2 py-1 rounded-full text-xs font-medium flex items-center ${
                          article.sensationalism_label === 'factual' 
                            ? 'bg-green-100 text-green-800' 
                            : article.sensationalism_label === 'somewhat sensational'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-orange-100 text-orange-800'
                        }`}
                      >
                        {article.sensationalism_label}
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="mt-1 flex items-center text-sm text-gray-500">
                  {article.source_name && (
                    <span className="mr-3">{article.source_name}</span>
                  )}
                  {article.published_at && (
                    <span>{new Date(article.published_at).toLocaleDateString()}</span>
                  )}
                </div>
                
                {article.description && (
                  <p className="mt-2 text-gray-600">{article.description}</p>
                )}
                
                <div className="mt-3 flex items-center justify-between">
                  <div>
                    <Link 
                      to={`/articles/${article.id}`}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium mr-4"
                    >
                      View Details
                    </Link>
                    
                    <a 
                      href={article.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-gray-600 hover:text-gray-800 text-sm"
                    >
                      Read Original &rarr;
                    </a>
                  </div>
                  
                  {/* Analysis timestamp or analyze button */}
                  {article.last_analyzed_at ? (
                    <span className="text-xs text-gray-500">
                      Analyzed: {new Date(article.last_analyzed_at).toLocaleString()}
                    </span>
                  ) : (
                    <button
                      onClick={() => handleAnalyzeArticle(article.id)}
                      className="text-xs text-gray-600 hover:text-gray-900 bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded"
                    >
                      Analyze
                    </button>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div className="p-6 text-center text-gray-500">
              {articleList.items.length > 0 
                ? 'No articles match the current filters.' 
                : 'No articles found for this topic.'}
            </div>
          )}
        </div>
      </div>

      {/* Pagination */}
      {articleList.pages > 1 && (
        <div className="flex justify-center">
          <nav className="inline-flex rounded-md shadow">
            <button
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
              className={`px-3 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium ${
                currentPage === 1
                  ? 'text-gray-300 cursor-not-allowed'
                  : 'text-gray-700 hover:bg-gray-50'
              }`}
            >
              Previous
            </button>
            
            {Array.from({ length: articleList.pages }, (_, i) => i + 1).map((page) => (
              <button
                key={page}
                onClick={() => handlePageChange(page)}
                className={`px-3 py-2 border border-gray-300 ${
                  currentPage === page
                    ? 'bg-blue-50 text-blue-600 z-10 border-blue-500'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                {page}
              </button>
            ))}
            
            <button
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === articleList.pages}
              className={`px-3 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium ${
                currentPage === articleList.pages
                  ? 'text-gray-300 cursor-not-allowed'
                  : 'text-gray-700 hover:bg-gray-50'
              }`}
            >
              Next
            </button>
          </nav>
        </div>
      )}
    </div>
  );
};

export default TopicDetail;