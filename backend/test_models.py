# Test script for database models
import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from app.db.base import SessionLocal
from app.models.source import Source
from app.models.article import Article
from app.models.topic import Topic, TopicArticle

def test_create_source_article_topic():
    """Test creating related source, article, and topic."""
    db = SessionLocal()
    
    try:
        # Create a source
        source = Source(
            url="https://example.com",
            title="Example Source",
            description="An example source for testing",
            source_type="test"
        )
        db.add(source)
        db.flush()  # Flush to get the ID without committing
        
        print(f"Created source: {source.title} (ID: {source.id})")
        
        # Create a topic
        topic = Topic(
            name="test topic",
            description="A test topic"
        )
        db.add(topic)
        db.flush()
        
        print(f"Created topic: {topic.name} (ID: {topic.id})")
        
        # Create an article associated with the source and topic
        article = Article(
            title="Test Article",
            url="https://example.com/article1",
            description="A test article",
            content="This is the content of the test article.",
            author="Test Author",
            published_at=datetime.now(),
            source_id=source.id,
            source_name=source.title
        )
        db.add(article)
        db.flush()
        
        print(f"Created article: {article.title} (ID: {article.id})")
        
        # Create the association between article and topic
        topic_article = TopicArticle(
            topic_id=topic.id,
            article_id=article.id,
            relevance_score=10  # High relevance
        )
        db.add(topic_article)
        
        # Commit the transaction
        db.commit()
        
        print("Successfully created related entities and committed to database")
        
        # Query to verify
        result_article = db.query(Article).filter(Article.id == article.id).first()
        print(f"Article from query: {result_article.title}")
        print(f"Article's source: {result_article.source.title}")
        print(f"Article's topics: {[t.name for t in result_article.topics]}")
        
        result_topic = db.query(Topic).filter(Topic.id == topic.id).first()
        print(f"Topic from query: {result_topic.name}")
        print(f"Topic's articles: {[a.title for a in result_topic.articles]}")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"Error in test: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("Testing database models...")
    
    success = test_create_source_article_topic()
    
    if success:
        print("\nAll tests passed!")
    else:
        print("\nTests failed.")