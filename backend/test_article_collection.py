# Test script for article collection service
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from app.db.base import SessionLocal
from app.services.article_collection import article_collection_service
from app.models.topic import Topic
from app.models.article import Article

def test_collect_articles():
    """Test collecting articles for a topic."""
    db = SessionLocal()
    
    try:
        # Choose a test topic
        test_topic = "artificial intelligence"
        
        print(f"\nCollecting articles for topic: {test_topic}")
        
        # Collect articles
        result = article_collection_service.collect_articles_for_topic(
            db=db,
            topic_name=test_topic,
            max_articles=10  # Limit to 10 articles to save API calls
        )
        
        # Print the results
        print("\nCollection Results:")
        print(f"Topic: {result['topic']}")
        print(f"Articles found: {result['articles_found']}")
        print(f"Articles stored: {result['articles_stored']}")
        print(f"Sources found: {result['sources_found']}")
        print(f"Sources stored: {result['sources_stored']}")
        
        if result['errors']:
            print("\nErrors:")
            for error in result['errors']:
                print(f"- {error}")
        
        # Verify the topic was created
        topic = db.query(Topic).filter(Topic.name == test_topic.lower()).first()
        if topic:
            print(f"\nTopic in database: {topic.name}")
            print(f"Search count: {topic.search_count}")
            print(f"Last searched: {topic.last_searched_at}")
            
            # Get the articles for this topic
            articles = db.query(Article).join(
                Article.topic_articles
            ).filter(
                Article.topic_articles.any(topic_id=topic.id)
            ).all()
            
            print(f"\nArticles for topic ({len(articles)}):")
            for i, article in enumerate(articles[:5], 1):  # Show only first 5
                print(f"\n{i}. {article.title}")
                print(f"   Source: {article.source_name}")
                print(f"   URL: {article.url}")
                print(f"   Published: {article.published_at}")
        else:
            print("\nTopic not found in database!")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"Error in test: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("Testing article collection...")
    
    success = test_collect_articles()
    
    if success:
        print("\nTest completed!")
    else:
        print("\nTest failed.")