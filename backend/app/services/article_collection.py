from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.source import Source
from app.models.article import Article
from app.models.topic import Topic, TopicArticle
from app.services.external.news_api import news_api_service

class ArticleCollectionService:
    """Service for collecting articles about topics and storing them in the database."""
    
    def collect_articles_for_topic(
        self, 
        db: Session, 
        topic_name: str, 
        max_articles: int = 20
    ) -> Dict[str, Any]:
        """
        Collect articles about a topic and store them in the database.
        
        Args:
            db: Database session
            topic_name: Name of the topic to collect articles for
            max_articles: Maximum number of articles to collect
            
        Returns:
            Dict containing information about the collection process
        """
        # Initialize result stats
        result = {
            "topic": topic_name,
            "articles_found": 0,
            "articles_stored": 0,
            "sources_found": 0,
            "sources_stored": 0,
            "errors": []
        }
        
        try:
            # Get or create the topic
            topic = self._get_or_create_topic(db, topic_name)
            
            # Update topic search stats
            topic.search_count += 1
            topic.last_searched_at = datetime.now()
            
            # Fetch articles from NewsAPI
            news_data = news_api_service.search_everything(
                query=topic_name,
                page_size=max_articles
            )
            
            # Process the articles
            processed_articles = news_api_service.process_articles(news_data)
            result["articles_found"] = len(processed_articles)
            
            # Set to track unique sources
            source_names = set()
            
            # Store each article
            for article_data in processed_articles:
                try:
                    # Track unique sources
                    if article_data["source_name"]:
                        source_names.add(article_data["source_name"])
                    
                    # Store the article
                    article = self._store_article(db, article_data, topic)
                    
                    if article:
                        result["articles_stored"] += 1
                except Exception as e:
                    result["errors"].append(f"Error storing article {article_data.get('title', 'unknown')}: {str(e)}")
            
            # Update source stats
            result["sources_found"] = len(source_names)
            
            # Count stored sources
            result["sources_stored"] = db.query(Source).filter(
                Source.title.in_(source_names)
            ).count()
            
            # Commit the transaction
            db.commit()
            
        except Exception as e:
            db.rollback()
            result["errors"].append(f"Error collecting articles: {str(e)}")
        
        return result
    
    def _get_or_create_topic(self, db: Session, topic_name: str) -> Topic:
        """
        Get a topic by name or create it if it doesn't exist.
        
        Args:
            db: Database session
            topic_name: Name of the topic
            
        Returns:
            Topic object
        """
        # Normalize topic name to lowercase for consistency
        normalized_name = topic_name.lower().strip()
        
        # Check if topic exists
        topic = db.query(Topic).filter(Topic.name == normalized_name).first()
        
        # If not, create it
        if not topic:
            topic = Topic(
                name=normalized_name,
                search_count=0
            )
            db.add(topic)
            db.flush()
        
        return topic
    
    def _get_or_create_source(self, db: Session, source_name: str, source_url: Optional[str] = None) -> Optional[Source]:
        """
        Get a source by name or create it if it doesn't exist.
        
        Args:
            db: Database session
            source_name: Name of the source
            source_url: URL of the source (optional)
            
        Returns:
            Source object or None if source_name is None
        """
        if not source_name:
            return None
        
        # Check if source exists by name
        source = db.query(Source).filter(Source.title == source_name).first()
        
        # If not, create it
        if not source:
            # Create a source URL if none provided
            url = source_url or f"https://{source_name.lower().replace(' ', '')}.com"
            
            source = Source(
                url=url,
                title=source_name,
                source_type="news",  # Default type
                description=f"Source: {source_name}"
            )
            db.add(source)
            db.flush()
        
        return source
    
    def _store_article(self, db: Session, article_data: Dict[str, Any], topic: Topic) -> Optional[Article]:
        """
        Store an article in the database and link it to a topic.
        
        Args:
            db: Database session
            article_data: Processed article data
            topic: Topic to link the article to
            
        Returns:
            Article object or None if there was an error
        """
        # Check if article already exists by URL
        existing_article = db.query(Article).filter(Article.url == article_data["url"]).first()
        
        if existing_article:
            # If article exists, link it to the topic if not already linked
            if topic not in existing_article.topics:
                topic_article = TopicArticle(
                    topic_id=topic.id,
                    article_id=existing_article.id
                )
                db.add(topic_article)
                db.flush()
            
            return existing_article
        
        # Get or create the source
        source = self._get_or_create_source(db, article_data["source_name"])
        
        # Parse published_at date if it exists
        published_at = None
        if article_data.get("published_at"):
            try:
                published_at = datetime.fromisoformat(article_data["published_at"].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                # If date parsing fails, default to current time
                published_at = datetime.now()
        
        # Create the article
        article = Article(
            title=article_data["title"],
            url=article_data["url"],
            description=article_data.get("description"),
            content=article_data.get("content"),
            author=article_data.get("author"),
            published_at=published_at,
            image_url=article_data.get("image_url"),
            source_id=source.id if source else None,
            source_name=article_data["source_name"]
        )
        
        # Add the article to the database
        db.add(article)
        db.flush()
        
        # Link the article to the topic
        topic_article = TopicArticle(
            topic_id=topic.id,
            article_id=article.id
        )
        db.add(topic_article)
        db.flush()
        
        return article

# Create a singleton instance for use throughout the application
article_collection_service = ArticleCollectionService()