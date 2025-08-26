import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { topicApi } from '../services/api';
import { SearchOverlay } from '../components/BackendStatusBanner';
import { useBackendHealth } from '../hooks/useBackendHealth';
import type { Topic, Article } from '../types/api';

const Search: React.FC = () => {
  const navigate = useNavigate();
  const { isHealthy } = useBackendHealth();
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchError, setSearchError] = useState<string | null>(null);
  const [searchResult, setSearchResult] = useState<{
    topic: Topic;
    articles: Article[];
    totalArticles: number;
  } | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!searchQuery.trim()) return;
    
    // Don't allow search if backend isn't ready
    if (!isHealthy) {
      setSearchError('Backend is still starting up. Please wait a moment and try again.');
      return;
    }
    
    setIsSearching(true);
    setSearchError(null);
    
    try {
      // Search for the topic
      const result = await topicApi.searchTopic({
        topic: searchQuery,
        max_articles: 20
      });
      
      // Get the articles for this topic
      const articles = await topicApi.getTopicArticles(result.topic.id, {
        page: 1,
        size: 10
      });
      
      // Store the result
      setSearchResult({
        topic: result.topic,
        articles: articles.items,
        totalArticles: articles.total
      });
    } catch (error) {
      console.error('Search error:', error);
      setSearchError('An error occurred while searching. Please try again.');
    } finally {
      setIsSearching(false);
    }
  };

  const handleViewTopic = (topicId: number) => {
    navigate(`/topics/${topicId}`);
  };

  return (
    <div className="container mx-auto px-4">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Search</h1>
      
      {/* Search form - wrapped with backend health overlay */}
      <SearchOverlay isBackendReady={isHealthy}>
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <form onSubmit={handleSearch}>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Enter a topic to search for (e.g., artificial intelligence, climate change)"
                className="flex-grow px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                disabled={!isHealthy}
              />
              <button 
                type="submit" 
                className={`font-medium px-4 py-2 rounded-md transition-colors flex items-center ${
                  !isHealthy 
                    ? 'bg-gray-400 cursor-not-allowed text-gray-700' 
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                }`}
                disabled={isSearching || !isHealthy}
              >
                {isSearching ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Searching...
                  </>
                ) : !isHealthy ? (
                  <>
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Backend Starting...
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    Search
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </SearchOverlay>
      
      {/* Error message */}
      {searchError && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
          <p className="font-bold">Error</p>
          <p>{searchError}</p>
        </div>
      )}
      
      {/* Search results */}
      {searchResult && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {/* Topic header */}
          <div className="bg-blue-50 p-6 border-b border-blue-100">
            <h2 className="text-2xl font-bold text-gray-900">{searchResult.topic.name}</h2>
            <div className="flex flex-wrap gap-4 mt-2 text-sm text-gray-600">
              <div>Searched {searchResult.topic.search_count} times</div>
              <div>{searchResult.totalArticles} articles found</div>
            </div>
            <button
              onClick={() => handleViewTopic(searchResult.topic.id)}
              className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-md transition-colors"
            >
              View Topic Analysis
            </button>
          </div>
          
          {/* Articles list */}
          <div className="divide-y divide-gray-200">
            {searchResult.articles.length > 0 ? (
              searchResult.articles.map((article) => (
                <div key={article.id} className="p-6">
                  <h3 className="text-lg font-medium text-gray-900">
                    <a 
                      href={article.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="hover:text-blue-600"
                    >
                      {article.title}
                    </a>
                  </h3>
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
                </div>
              ))
            ) : (
              <div className="p-6 text-center text-gray-500">
                No articles found for this topic.
              </div>
            )}
          </div>
          
          {/* View more link */}
          {searchResult.totalArticles > searchResult.articles.length && (
            <div className="p-4 bg-gray-50 text-center">
              <button
                onClick={() => handleViewTopic(searchResult.topic.id)}
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                View all {searchResult.totalArticles} articles
              </button>
            </div>
          )}
        </div>
      )}
      
      {/* Empty state */}
      {!isSearching && !searchError && !searchResult && (
        <div className="bg-white rounded-lg shadow p-6 text-center py-12">
          <svg className="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <p className="text-gray-500">Search for a topic to see results</p>
          <p className="text-gray-500 text-sm mt-1">Enter a topic like "artificial intelligence" or "climate change"</p>
          {!isHealthy && (
            <p className="text-amber-600 text-sm mt-2 font-medium">
              Search will be available once the backend finishes starting up
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default Search;