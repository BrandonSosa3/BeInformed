"""
Statistics Service

This module provides functionality for calculating aggregate statistics
about topics, articles, and sources for visualization purposes.
"""

from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
from sqlalchemy import func, case, distinct, and_, or_
from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.topic import Topic, TopicArticle
from app.models.source import Source

# Set up logging
logger = logging.getLogger(__name__)

class StatisticsService:
    """Service for calculating aggregate statistics for visualization."""
    
    def get_topic_statistics(self, db: Session, topic_id: int, days: int = 30) -> Dict[str, Any]:
        """
        Get aggregate statistics for a topic.
        
        Args:
            db: Database session
            topic_id: ID of the topic
            days: Number of days to include in statistics (0 for all time)
            
        Returns:
            Dict with topic statistics
        """
        try:
            # Get the topic
            topic = db.query(Topic).filter(Topic.id == topic_id).first()
            if not topic:
                logger.error(f"Topic with ID {topic_id} not found")
                return self._empty_stats()
            
            # Debug: Log topic details
            logger.info(f"Getting statistics for topic: {topic.name} (ID: {topic_id})")
            
            # Define time range filter
            date_filter = True  # Default to all articles
            time_range_str = "all time"
            
            if days > 0:
                cutoff_date = datetime.now() - timedelta(days=days)
                date_filter = Article.published_at >= cutoff_date
                time_range_str = f"last {days} days"
            
            # Get all articles associated with this topic
            topic_article_query = db.query(TopicArticle.article_id).filter(TopicArticle.topic_id == topic_id)
            article_ids = [ta.article_id for ta in topic_article_query.all()]
            
            logger.info(f"Found {len(article_ids)} article IDs for topic {topic_id}")
            
            if not article_ids:
                return self._empty_stats()
            
            # Count total articles using the article IDs directly
            total_articles = len(article_ids)
            
            # Count analyzed articles
            analyzed_articles = db.query(func.count(Article.id)).filter(
                Article.id.in_(article_ids),
                Article.last_analyzed_at.isnot(None),
                date_filter
            ).scalar() or 0
            
            logger.info(f"Total articles: {total_articles}, Analyzed: {analyzed_articles}")
            
            # Only continue with other calculations if we have analyzed articles
            if analyzed_articles > 0:
                # Calculate average sentiment
                avg_sentiment = db.query(func.avg(Article.sentiment_score)).filter(
                    Article.id.in_(article_ids),
                    Article.sentiment_score.isnot(None),
                    date_filter
                ).scalar() or 0
                
                # Get sentiment distribution
                sentiment_distribution = self._get_sentiment_distribution_by_ids(db, article_ids, date_filter)
                
                # Get bias distribution
                bias_distribution = self._get_bias_distribution_by_ids(db, article_ids, date_filter)
                
                # Count sources
                sources_count = db.query(func.count(distinct(Article.source_id))).filter(
                    Article.id.in_(article_ids),
                    Article.source_id.isnot(None),
                    date_filter
                ).scalar() or 0
                
                # Calculate average sensationalism
                avg_sensationalism = db.query(func.avg(Article.sensationalism_score)).filter(
                    Article.id.in_(article_ids),
                    Article.sensationalism_score.isnot(None),
                    date_filter
                ).scalar() or 0
            else:
                # Default values if no analyzed articles
                avg_sentiment = 0
                sentiment_distribution = {"positive": 0, "neutral": 0, "negative": 0}
                bias_distribution = {"leftLeaning": 0, "centrist": 0, "rightLeaning": 0}
                sources_count = 0
                avg_sensationalism = 0
            
            # Return compiled statistics
            return {
                "totalArticles": total_articles,
                "analyzedArticles": analyzed_articles,
                "averageSentiment": round(float(avg_sentiment or 0), 2),
                "sentimentDistribution": sentiment_distribution,
                "biasDistribution": bias_distribution,
                "sourcesCount": sources_count,
                "sensationalismLevel": round(float(avg_sensationalism or 0), 2),
                "timeRange": time_range_str
            }
            
        except Exception as e:
            logger.error(f"Error getting topic statistics: {str(e)}")
            return self._empty_stats()
    
    def _get_sentiment_distribution(self, db: Session, topic_id: int, date_filter) -> Dict[str, int]:
        """
        Get the distribution of sentiment labels for a topic using topic_id.
        
        Args:
            db: Database session
            topic_id: ID of the topic
            date_filter: Date filter condition
            
        Returns:
            Dict with counts for each sentiment label
        """
        # Define conditions for each sentiment category
        positive_condition = Article.sentiment_label == 'positive'
        neutral_condition = Article.sentiment_label == 'neutral'
        negative_condition = Article.sentiment_label == 'negative'
        
        # Query for counts of each category
        sentiment_counts = db.query(
            func.sum(case([(positive_condition, 1)], else_=0)).label('positive'),
            func.sum(case([(neutral_condition, 1)], else_=0)).label('neutral'),
            func.sum(case([(negative_condition, 1)], else_=0)).label('negative')
        ).join(
            TopicArticle
        ).filter(
            TopicArticle.topic_id == topic_id,
            Article.sentiment_label.isnot(None),
            date_filter
        ).first()
        
        # Extract counts from result
        if sentiment_counts:
            return {
                "positive": int(sentiment_counts.positive or 0),
                "neutral": int(sentiment_counts.neutral or 0),
                "negative": int(sentiment_counts.negative or 0)
            }
        else:
            return {"positive": 0, "neutral": 0, "negative": 0}
    
    def _get_sentiment_distribution_by_ids(self, db: Session, article_ids: List[int], date_filter) -> Dict[str, int]:
        """
        Get the distribution of sentiment labels for articles by their IDs.
        
        Args:
            db: Database session
            article_ids: List of article IDs
            date_filter: Date filter condition
            
        Returns:
            Dict with counts for each sentiment label
        """
        # Define conditions for each sentiment category
        positive_condition = Article.sentiment_label == 'positive'
        neutral_condition = Article.sentiment_label == 'neutral'
        negative_condition = Article.sentiment_label == 'negative'
        
        # Query for counts of each category
        sentiment_counts = db.query(
            func.sum(case([(positive_condition, 1)], else_=0)).label('positive'),
            func.sum(case([(neutral_condition, 1)], else_=0)).label('neutral'),
            func.sum(case([(negative_condition, 1)], else_=0)).label('negative')
        ).filter(
            Article.id.in_(article_ids),
            Article.sentiment_label.isnot(None),
            date_filter
        ).first()
        
        # Extract counts from result
        if sentiment_counts:
            return {
                "positive": int(sentiment_counts.positive or 0),
                "neutral": int(sentiment_counts.neutral or 0),
                "negative": int(sentiment_counts.negative or 0)
            }
        else:
            return {"positive": 0, "neutral": 0, "negative": 0}
    
    def _get_bias_distribution(self, db: Session, topic_id: int, date_filter) -> Dict[str, int]:
        """
        Get the distribution of political bias labels for a topic using topic_id.
        
        Args:
            db: Database session
            topic_id: ID of the topic
            date_filter: Date filter condition
            
        Returns:
            Dict with counts for each bias label
        """
        # Define conditions for each bias category
        left_condition = Article.political_bias_label == 'left-leaning'
        centrist_condition = or_(
            Article.political_bias_label == 'centrist',
            Article.political_bias_label == 'neutral'
        )
        right_condition = Article.political_bias_label == 'right-leaning'
        
        # Query for counts of each category
        bias_counts = db.query(
            func.sum(case([(left_condition, 1)], else_=0)).label('left_leaning'),
            func.sum(case([(centrist_condition, 1)], else_=0)).label('centrist'),
            func.sum(case([(right_condition, 1)], else_=0)).label('right_leaning')
        ).join(
            TopicArticle
        ).filter(
            TopicArticle.topic_id == topic_id,
            Article.political_bias_label.isnot(None),
            date_filter
        ).first()
        
        # Extract counts from result
        if bias_counts:
            return {
                "leftLeaning": int(bias_counts.left_leaning or 0),
                "centrist": int(bias_counts.centrist or 0),
                "rightLeaning": int(bias_counts.right_leaning or 0)
            }
        else:
            return {"leftLeaning": 0, "centrist": 0, "rightLeaning": 0}
    
    def _get_bias_distribution_by_ids(self, db: Session, article_ids: List[int], date_filter) -> Dict[str, int]:
        """
        Get the distribution of political bias labels for articles by their IDs.
        
        Args:
            db: Database session
            article_ids: List of article IDs
            date_filter: Date filter condition
            
        Returns:
            Dict with counts for each bias label
        """
        # Define conditions for each bias category
        left_condition = Article.political_bias_label == 'left-leaning'
        centrist_condition = or_(
            Article.political_bias_label == 'centrist',
            Article.political_bias_label == 'neutral'
        )
        right_condition = Article.political_bias_label == 'right-leaning'
        
        # Query for counts of each category
        bias_counts = db.query(
            func.sum(case([(left_condition, 1)], else_=0)).label('left_leaning'),
            func.sum(case([(centrist_condition, 1)], else_=0)).label('centrist'),
            func.sum(case([(right_condition, 1)], else_=0)).label('right_leaning')
        ).filter(
            Article.id.in_(article_ids),
            Article.political_bias_label.isnot(None),
            date_filter
        ).first()
        
        # Extract counts from result
        if bias_counts:
            return {
                "leftLeaning": int(bias_counts.left_leaning or 0),
                "centrist": int(bias_counts.centrist or 0),
                "rightLeaning": int(bias_counts.right_leaning or 0)
            }
        else:
            return {"leftLeaning": 0, "centrist": 0, "rightLeaning": 0}
    
    def _empty_stats(self) -> Dict[str, Any]:
        """Return empty statistics structure."""
        return {
            "totalArticles": 0,
            "analyzedArticles": 0,
            "averageSentiment": 0,
            "sentimentDistribution": {"positive": 0, "neutral": 0, "negative": 0},
            "biasDistribution": {"leftLeaning": 0, "centrist": 0, "rightLeaning": 0},
            "sourcesCount": 0,
            "sensationalismLevel": 0,
            "timeRange": "all time"
        }
    
    def get_source_statistics(self, db: Session, topic_id: int) -> List[Dict[str, Any]]:
        """
        Get statistics about sources for a topic.
        
        Args:
            db: Database session
            topic_id: ID of the topic
            
        Returns:
            List of sources with statistics
        """
        try:
            # Get all article IDs for this topic
            topic_article_query = db.query(TopicArticle.article_id).filter(TopicArticle.topic_id == topic_id)
            article_ids = [ta.article_id for ta in topic_article_query.all()]
            
            if not article_ids:
                return []
            
            # Get articles for this topic grouped by source
            source_stats = db.query(
                Article.source_id,
                Article.source_name,
                func.count(Article.id).label('article_count'),
                func.avg(Article.sentiment_score).label('avg_sentiment'),
                func.avg(Article.political_bias_score).label('avg_bias'),
                func.avg(Article.sensationalism_score).label('avg_sensationalism')
            ).filter(
                Article.id.in_(article_ids),
                Article.source_name.isnot(None)
            ).group_by(
                Article.source_id, 
                Article.source_name
            ).all()
            
            # Format results
            result = []
            for stat in source_stats:
                source_data = {
                    "sourceId": stat.source_id,
                    "sourceName": stat.source_name,
                    "articleCount": stat.article_count,
                    "averageSentiment": round(float(stat.avg_sentiment or 0), 2),
                    "averageBias": round(float(stat.avg_bias or 0), 2),
                    "averageSensationalism": round(float(stat.avg_sensationalism or 0), 2)
                }
                result.append(source_data)
            
            # Sort by article count (descending)
            result.sort(key=lambda x: x["articleCount"], reverse=True)
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting source statistics: {str(e)}")
            return []
    
    def get_sentiment_over_time(
        self, 
        db: Session, 
        topic_id: int, 
        days: int = 30,
        interval: str = 'day'
    ) -> Dict[str, Any]:
        """
        Get sentiment trends over time for a topic.
        
        Args:
            db: Database session
            topic_id: ID of the topic
            days: Number of days to include
            interval: Time interval for grouping ('day', 'week', 'month')
            
        Returns:
            Dict with dates and sentiment values
        """
        try:
            # Get all article IDs for this topic
            topic_article_query = db.query(TopicArticle.article_id).filter(TopicArticle.topic_id == topic_id)
            article_ids = [ta.article_id for ta in topic_article_query.all()]
            
            if not article_ids:
                return {"dates": [], "sentiment": [], "counts": []}
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Build the date grouping expression based on interval
            if interval == 'week':
                # Group by week (date_trunc not used for compatibility)
                date_expr = func.date(Article.published_at)
            elif interval == 'month':
                # Group by month
                date_expr = func.date(Article.published_at)
            else:
                # Default to day
                date_expr = func.date(Article.published_at)
            
            # Query for sentiment by date
            sentiment_data = db.query(
                date_expr.label('date'),
                func.avg(Article.sentiment_score).label('avg_sentiment'),
                func.count(Article.id).label('article_count')
            ).filter(
                Article.id.in_(article_ids),
                Article.published_at >= start_date,
                Article.published_at <= end_date,
                Article.sentiment_score.isnot(None)
            ).group_by(
                date_expr
            ).order_by(
                date_expr
            ).all()
            
            # Format results
            dates = []
            sentiment_values = []
            article_counts = []
            
            for item in sentiment_data:
                dates.append(item.date.isoformat() if item.date else None)
                sentiment_values.append(round(float(item.avg_sentiment or 0), 2))
                article_counts.append(item.article_count)
            
            return {
                "dates": dates,
                "sentiment": sentiment_values,
                "counts": article_counts
            }
            
        except Exception as e:
            logger.error(f"Error getting sentiment over time: {str(e)}")
            return {"dates": [], "sentiment": [], "counts": []}

# Create a singleton instance for use throughout the application
statistics_service = StatisticsService()