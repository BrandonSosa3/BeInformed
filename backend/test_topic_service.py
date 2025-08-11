# Test script for topic service
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from app.db.base import SessionLocal
from app.services.topic import topic_service

def test_search_or_create_topic():
    """Test searching or creating a topic and collecting articles."""
    db = SessionLocal()
    
    try:
        # Choose a test topic
        test_topic = "machine learning"
        
        print(f"\nSearching or creating topic: {test_topic}")
        
        # Search or create the topic and collect articles
        result = topic_service.search_or_create_topic(
            db=db,
            topic_name=test_topic,
            collect_articles=True,
            max_articles=10  # Limit to 10 articles to save API calls
        )
        
        # Print the results
        topic = result["topic"]
        print(f"\nTopic: {topic.name}")
        print(f"ID: {topic.id}")
        print(f"Is new: {result['is_new']}")
        print(f"Search count: {topic.search_count}")
        print(f"Last searched: {topic.last_searched_at}")
        
        if result["collection_result"]:
            collection = result["collection_result"]
            print(f"\nArticles found: {collection['articles_found']}")
            print(f"Articles stored: {collection['articles_stored']}")
            print(f"Sources found: {collection['sources_found']}")
            print(f"Sources stored: {collection['sources_stored']}")
        
        # Get articles for the topic
        articles = topic_service.get_topic_articles(
            db=db,
            topic_id=topic.id,
            limit=5  # Get only 5 articles
        )
        
        print(f"\nArticles for topic ({len(articles)}):")
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article.title}")
            print(f"   Source: {article.source_name}")
            print(f"   Published: {article.published_at}")
        
        # Get popular topics
        popular_topics = topic_service.get_topics(
            db=db,
            limit=5,
            sort_by="search_count"
        )
        
        print(f"\nPopular topics ({len(popular_topics)}):")
        for i, topic in enumerate(popular_topics, 1):
            print(f"{i}. {topic.name} (searched {topic.search_count} times)")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"Error in test: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("Testing topic service...")
    
    success = test_search_or_create_topic()
    
    if success:
        print("\nTest completed!")
    else:
        print("\nTest failed.")