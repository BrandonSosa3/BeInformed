import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { topicApi } from '../services/api';
import type{ Topic, Article, ArticleList } from '../types/api';

const TopicDetail: React.FC = () => {
  const { topicId } = useParams<{ topicId: string }>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [topic, setTopic] = useState<Topic | null>(null);
  const [articleList, setArticleList] = useState<ArticleList | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  
  useEffect(() => {
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
    
    fetchTopic();
  }, [topicId, currentPage]);
  
  const handlePageChange = (page: number) => {
    if (page >= 1 && (!articleList || page <= articleList.pages)) {
      setCurrentPage(page);
    }
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
      </div>
      
      {/* Articles list */}
      <div className="bg-white rounded-lg shadow overflow-hidden mb-6">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-800">Articles</h2>
        </div>
        
        <div className="divide-y divide-gray-200">
          {articleList.items.length > 0 ? (
            articleList.items.map((article) => (
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
                <div className="mt-3 flex items-center">
                  <a 
                    href={article.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    Read Article &rarr;
                  </a>
                </div>
              </div>
            ))
          ) : (
            <div className="p-6 text-center text-gray-500">
              No articles found for this topic.
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