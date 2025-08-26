import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { articleApi } from '../services/api';
import type { Article } from '../types/api';
import ArticleSummary from '../components/layout/ArticleSummary';
import BadgesLegend from '../components/BadgesLegend';

const ArticleDetail: React.FC = () => {
  const { articleId } = useParams<{ articleId: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [article, setArticle] = useState<Article | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  
  useEffect(() => {
    const fetchArticle = async () => {
      setLoading(true);
      setError(null);
      
      try {
        if (!articleId) {
          throw new Error('Article ID is required');
        }
        
        const articleData = await articleApi.getArticle(parseInt(articleId));
        setArticle(articleData);
      } catch (err) {
        console.error('Error fetching article:', err);
        setError('Failed to load article data. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchArticle();
  }, [articleId]);
  
  const handleAnalyze = async () => {
    if (!articleId) return;
    
    setAnalyzing(true);
    
    try {
      // Call the analysis API
      await fetch(`http://localhost:8000/api/v1/analysis/articles/${articleId}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      // Refresh the article data
      const articleData = await articleApi.getArticle(parseInt(articleId));
      setArticle(articleData);
    } catch (err) {
      console.error('Error analyzing article:', err);
      setError('Failed to analyze article. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };
  
  // Enhanced function to clean content - remove anything that looks like a summary
  const cleanContent = (content: string | null): string => {
    if (!content) return '';
    
    // If content is very short (less than 300 chars), it's probably just a summary
    if (content.length < 300) return '';
    
    // Remove truncation marker and anything before it
    if (content.includes("[+")) {
      const parts = content.split("[+");
      // If first part contains the title or is very short, remove it
      if (article?.title && (
          parts[0].includes(article.title) || 
          parts[0].length < 200)
      ) {
        return ''; // Return empty
      }
      return parts[0].trim(); // Just return the content without the truncation marker
    }
    
    // If content starts with the title or description, it might be a summary
    if (article?.title && content.startsWith(article.title)) {
      return ''; // Return empty
    }
    
    if (article?.description && content.startsWith(article.description)) {
      return ''; // Return empty
    }
    
    // If content contains phrases like "Read more" or has fewer than 3 sentences, 
    // it might be a truncated preview
    if (
      content.includes("Read more") || 
      content.includes("...") || 
      content.split(". ").length < 3
    ) {
      return '';
    }
    
    return content;
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
  
  if (error || !article) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
          <p className="font-bold">Error</p>
          <p>{error || 'Failed to load article data.'}</p>
        </div>
        <button
          onClick={() => navigate(-1)}
          className="text-blue-600 hover:text-blue-800"
        >
          &larr; Go Back
        </button>
      </div>
    );
  }
  
  // Clean the content to remove any summary-like parts
  const cleanedContent = cleanContent(article.content);
  
  return (
    <div className="container mx-auto px-4 py-8">
      {/* Back button */}
      <button
        onClick={() => navigate(-1)}
        className="text-blue-600 hover:text-blue-800 mb-6 inline-block"
      >
        &larr; Back
      </button>
      
      {/* Article header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{article.title}</h1>
        <div className="flex flex-wrap gap-2 mb-4">
          {/* Source and date */}
          <div className="text-gray-600">
            {article.source_name && <span className="mr-2">{article.source_name}</span>}
            {article.published_at && (
              <span>{new Date(article.published_at).toLocaleDateString()}</span>
            )}
          </div>
          
          {/* Analysis badges */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="flex flex-wrap gap-2">
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
            
            {/* Add BadgesLegend here */}
            <BadgesLegend />
          </div>
        </div>
        
        {/* Analyze button (show only if not analyzed) */}
        {!article.last_analyzed_at && (
          <button
            onClick={handleAnalyze}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium px-4 py-2 rounded-md transition-colors flex items-center"
            disabled={analyzing}
          >
            {analyzing ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </>
            ) : (
              <>Analyze Article</>
            )}
          </button>
        )}
      </div>
      
      {/* Article summary - positioned prominently before content */}
      {article && <ArticleSummary article={article} />}
      
      {/* Article image (if available) */}
      {article.image_url && (
        <div className="mb-6">
          <img
            src={article.image_url}
            alt={article.title}
            className="w-full h-auto rounded-lg shadow-md"
          />
        </div>
      )}
      
      {/* Article content - ONLY show if we have meaningful cleaned content */}
      {cleanedContent && cleanedContent.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="prose max-w-none">
            {cleanedContent.split('\n').map((paragraph, index) => (
              paragraph.trim() ? <p key={index} className="mb-4">{paragraph}</p> : null
            ))}
          </div>
        </div>
      )}
      
      {/* Read original link */}
      <div className="text-center mb-8">
        <a 
          href={article.url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="bg-gray-800 hover:bg-gray-900 text-white font-medium px-6 py-3 rounded-md transition-colors inline-block"
        >
          Read Original Article
        </a>
      </div>
      
      {/* Analysis timestamp */}
      {article.last_analyzed_at && (
        <div className="text-center text-sm text-gray-500 mb-8">
          Last analyzed: {new Date(article.last_analyzed_at).toLocaleString()}
        </div>
      )}
    </div>
  );
};

export default ArticleDetail;