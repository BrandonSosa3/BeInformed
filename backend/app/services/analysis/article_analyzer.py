"""
Article Analysis Service

This module provides functionality to analyze articles for sentiment,
bias, and other metrics, and update the database with the results.
"""

from typing import Dict, Any, List, Optional, Union
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.article import Article
from app.services.analysis.sentiment import sentiment_analysis_service
from app.services.analysis.bias import bias_detection_service

# Set up logging
logger = logging.getLogger(__name__)

class ArticleAnalysisService:
    """Service for analyzing articles and updating the database with results."""
    
    def __init__(self):
        """Initialize the article analysis service."""
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize the article analysis service and its dependencies.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        try:
            # Initialize sentiment analysis service
            sentiment_initialized = sentiment_analysis_service.initialize()
            
            # Initialize bias detection service
            bias_initialized = bias_detection_service.initialize()
            
            # In the future, we can initialize other analysis services here
            
            self.is_initialized = sentiment_initialized and bias_initialized
            if self.is_initialized:
                logger.info("Article analysis service initialized successfully")
            else:
                logger.error("Failed to initialize article analysis service")
                
            return self.is_initialized
        except Exception as e:
            logger.error(f"Error initializing article analysis service: {e}")
            return False
    
    def analyze_article(self, article: Union[Article, Dict[str, Any]], db: Optional[Session] = None) -> Dict[str, Any]:
        """
        Analyze an article and return the analysis results.
        
        Args:
            article: Article object or dictionary with article data
            db: Database session (optional, required for saving results)
            
        Returns:
            Dict[str, Any]: Dictionary with analysis results
        """
        if not self.is_initialized:
            self.initialize()
        
        # Convert Article object to dictionary if needed
        article_data = article
        if isinstance(article, Article):
            article_data = {
                "id": article.id,
                "title": article.title,
                "description": article.description,
                "content": article.content,
                "source_name": article.source_name
            }
        
        # Initialize results
        results = {
            "sentiment": None,
            "bias": None,
            "credibility": None,  # For future implementation
            "analysis_time": datetime.now()
        }
        
        try:
            # Perform sentiment analysis
            sentiment_result = sentiment_analysis_service.analyze_article(article_data)
            results["sentiment"] = sentiment_result
            
            # Perform bias detection
            bias_result = bias_detection_service.analyze_article(article_data)
            results["bias"] = bias_result
            
            # If a database session is provided and we have an Article object,
            # update the article in the database
            if db and isinstance(article, Article):
                self._update_article_with_results(db, article, sentiment_result, bias_result)
            
            return results
        except Exception as e:
            logger.error(f"Error analyzing article {article_data.get('id', 'unknown')}: {e}")
            return results
    
    def _update_article_with_results(
        self, 
        db: Session, 
        article: Article, 
        sentiment_result: Dict[str, Any],
        bias_result: Dict[str, Any]
    ) -> None:
        """
        Update an article with analysis results.
        
        Args:
            db: Database session
            article: Article object to update
            sentiment_result: Sentiment analysis results
            bias_result: Bias detection results
        """
        try:
            # Update article with sentiment data
            article.sentiment_score = sentiment_result["score"]
            article.sentiment_label = sentiment_result["label"]
            article.sentiment_confidence = sentiment_result["confidence"]
            
            # Update article with political bias data
            political_bias = bias_result["political_bias"]
            article.political_bias_score = political_bias["score"]
            article.political_bias_label = political_bias["label"]
            
            # Update article with sensationalism data
            sensationalism = bias_result["sensationalism"]
            article.sensationalism_score = sensationalism["score"]
            article.sensationalism_label = sensationalism["label"]
            
            # Store detailed bias data in the JSON field
            article.bias_scores = {
                "political": {
                    "score": political_bias["score"],
                    "label": political_bias["label"],
                    "confidence": political_bias["confidence"],
                },
                "sensationalism": {
                    "score": sensationalism["score"],
                    "label": sensationalism["label"],
                    "confidence": sensationalism["confidence"],
                }
            }
            
            # Update last analyzed timestamp
            article.last_analyzed_at = datetime.now()
            
            # Commit changes
            db.commit()
            logger.info(f"Updated article {article.id} with analysis results")
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating article {article.id} with analysis results: {e}")
    
    def analyze_articles_by_topic(self, db: Session, topic_id: int, limit: int = 100) -> Dict[str, Any]:
        """
        Analyze articles for a specific topic.
        
        Args:
            db: Database session
            topic_id: ID of the topic
            limit: Maximum number of articles to analyze
            
        Returns:
            Dict[str, Any]: Results of the analysis operation
        """
        from app.models.topic import Topic, TopicArticle
        
        if not self.is_initialized:
            self.initialize()
        
        results = {
            "topic_id": topic_id,
            "articles_analyzed": 0,
            "articles_updated": 0,
            "errors": [],
            "analysis_time": datetime.now()
        }
        
        try:
            # Get the topic
            topic = db.query(Topic).filter(Topic.id == topic_id).first()
            if not topic:
                results["errors"].append(f"Topic with ID {topic_id} not found")
                return results
            
            # Get articles for this topic that haven't been analyzed yet
            # or were analyzed more than 7 days ago
            one_week_ago = datetime.now() - timedelta(days=7)
            articles = db.query(Article).join(
                TopicArticle
            ).filter(
                TopicArticle.topic_id == topic_id,
                (Article.last_analyzed_at == None) | (Article.last_analyzed_at < one_week_ago)
            ).limit(limit).all()
            
            results["articles_found"] = len(articles)
            
            # Analyze each article
            for article in articles:
                try:
                    self.analyze_article(article, db)
                    results["articles_updated"] += 1
                except Exception as e:
                    error_msg = f"Error analyzing article {article.id}: {str(e)}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
                
                results["articles_analyzed"] += 1
            
            return results
        except Exception as e:
            error_msg = f"Error analyzing articles for topic {topic_id}: {str(e)}"
            logger.error(error_msg)
            results["errors"].append(error_msg)
            return results
    
    def analyze_recent_articles(self, db: Session, days: int = 7, limit: int = 100) -> Dict[str, Any]:
        """
        Analyze recent articles that haven't been analyzed yet.
        
        Args:
            db: Database session
            days: Number of days to look back
            limit: Maximum number of articles to analyze
            
        Returns:
            Dict[str, Any]: Results of the analysis operation
        """
        if not self.is_initialized:
            self.initialize()
        
        results = {
            "days": days,
            "articles_analyzed": 0,
            "articles_updated": 0,
            "errors": [],
            "analysis_time": datetime.now()
        }
        
        try:
            # Calculate the date threshold
            date_threshold = datetime.now() - timedelta(days=days)
            
            # Get recent articles that haven't been analyzed yet
            articles = db.query(Article).filter(
                Article.created_at >= date_threshold,
                (Article.last_analyzed_at == None) | 
                (Article.sentiment_score == None) |
                (Article.political_bias_score == None)
            ).limit(limit).all()
            
            results["articles_found"] = len(articles)
            
            # Analyze each article
            for article in articles:
                try:
                    self.analyze_article(article, db)
                    results["articles_updated"] += 1
                except Exception as e:
                    error_msg = f"Error analyzing article {article.id}: {str(e)}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
                
                results["articles_analyzed"] += 1
            
            return results
        except Exception as e:
            error_msg = f"Error analyzing recent articles: {str(e)}"
            logger.error(error_msg)
            results["errors"].append(error_msg)
            return results

# Create a singleton instance for use throughout the application
article_analysis_service = ArticleAnalysisService()