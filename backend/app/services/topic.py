from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.topic import Topic
from app.models.article import Article
from app.services.article_collection import article_collection_service

class TopicService:
    """Service for managing topics."""
    
    def get_topic(self, db: Session, topic_id: int) -> Optional[Topic]:
        """
        Get a topic by ID.
        
        Args:
            db: Database session
            topic_id: ID of the topic
            
        Returns:
            Topic object or None if not found
        """
        return db.query(Topic).filter(Topic.id == topic_id).first()
    
    def get_topic_by_name(self, db: Session, name: str) -> Optional[Topic]:
        """
        Get a topic by name.
        
        Args:
            db: Database session
            name: Name of the topic
            
        Returns:
            Topic object or None if not found
        """
        # Normalize name
        normalized_name = name.lower().strip()
        return db.query(Topic).filter(Topic.name == normalized_name).first()
    
    def get_topics(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        sort_by: str = "search_count"
    ) -> List[Topic]:
        """
        Get all topics with pagination and sorting.
        
        Args:
            db: Database session
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            sort_by: Field to sort by (search_count, name, created_at, last_searched_at)
            
        Returns:
            List of Topic objects
        """
        # Determine sort order
        if sort_by == "search_count":
            order_by = desc(Topic.search_count)
        elif sort_by == "name":
            order_by = Topic.name
        elif sort_by == "created_at":
            order_by = desc(Topic.created_at)
        elif sort_by == "last_searched_at":
            order_by = desc(Topic.last_searched_at)
        else:
            order_by = desc(Topic.search_count)  # Default
        
        return db.query(Topic).order_by(order_by).offset(skip).limit(limit).all()
    
    def search_or_create_topic(
        self, 
        db: Session, 
        topic_name: str,
        collect_articles: bool = True,
        max_articles: int = 20
    ) -> Dict[str, Any]:
        """
        Search for a topic by name or create it if it doesn't exist.
        Optionally collect articles for the topic.
        
        Args:
            db: Database session
            topic_name: Name of the topic
            collect_articles: Whether to collect articles for the topic
            max_articles: Maximum number of articles to collect
            
        Returns:
            Dict containing the topic and collection results
        """
        result = {
            "topic": None,
            "is_new": False,
            "collection_result": None
        }
        
        # Normalize topic name
        normalized_name = topic_name.lower().strip()
        
        # Check if topic exists
        topic = self.get_topic_by_name(db, normalized_name)
        
        # If not, create it
        if not topic:
            topic = Topic(
                name=normalized_name,
                search_count=0
            )
            db.add(topic)
            db.flush()
            result["is_new"] = True
        
        # Update topic search stats
        topic.search_count += 1
        topic.last_searched_at = Topic.last_searched_at = topic.last_searched_at
        
        # Store the topic in the result
        result["topic"] = topic
        
        # Collect articles if requested
        if collect_articles:
            result["collection_result"] = article_collection_service.collect_articles_for_topic(
                db=db,
                topic_name=topic_name,
                max_articles=max_articles
            )
        
        # Commit changes
        db.commit()
        
        return result
    
    def get_topic_articles(
        self, 
        db: Session, 
        topic_id: int,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "published_at"
    ) -> List[Article]:
        """
        Get articles for a topic with pagination and sorting.
        
        Args:
            db: Database session
            topic_id: ID of the topic
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            sort_by: Field to sort by (published_at, title, source_name)
            
        Returns:
            List of Article objects
        """
        # Base query
        query = db.query(Article).join(
            Article.topic_articles
        ).filter(
            Article.topic_articles.any(topic_id=topic_id)
        )
        
        # Apply sorting
        if sort_by == "published_at":
            query = query.order_by(desc(Article.published_at))
        elif sort_by == "title":
            query = query.order_by(Article.title)
        elif sort_by == "source_name":
            query = query.order_by(Article.source_name)
        else:
            query = query.order_by(desc(Article.published_at))  # Default
        
        # Apply pagination
        return query.offset(skip).limit(limit).all()

# Create a singleton instance for use throughout the application
topic_service = TopicService()