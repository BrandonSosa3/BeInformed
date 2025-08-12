# Test script for article analysis service
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from app.db.base import SessionLocal
from app.services.analysis.article_analyzer import article_analysis_service
from app.models.article import Article
from app.models.topic import Topic

def test_analyze_article():
    """Test analyzing a single article."""
    db = SessionLocal()
    
    try:
        # Get an article from the database
        article = db.query(Article).first()
        
        if not article:
            print("No articles found in the database. Please run the article collection test first.")
            return False
        
        print(f"\nAnalyzing article: {article.title}")
        print(f"Source: {article.source_name}")
        
        # Check if the article already has sentiment data
        if article.sentiment_score is not None:
            print(f"Article already has sentiment data:")
            print(f"  Score: {article.sentiment_score}")
            print(f"  Label: {article.sentiment_label}")
            print(f"  Confidence: {article.sentiment_confidence}")
            print(f"  Last analyzed: {article.last_analyzed_at}")
        
        # Analyze the article
        result = article_analysis_service.analyze_article(article, db)
        
        # Print the results
        print("\nAnalysis results:")
        if result["sentiment"]:
            print(f"Sentiment score: {result['sentiment']['score']}")
            print(f"Sentiment label: {result['sentiment']['label']}")
            print(f"Confidence: {result['sentiment']['confidence']}")
        
        # Verify the database was updated
        db.refresh(article)
        print("\nArticle in database after analysis:")
        print(f"  Sentiment score: {article.sentiment_score}")
        print(f"  Sentiment label: {article.sentiment_label}")
        print(f"  Confidence: {article.sentiment_confidence}")
        print(f"  Last analyzed: {article.last_analyzed_at}")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"Error in test: {e}")
        return False
    finally:
        db.close()

def test_analyze_topic_articles():
    """Test analyzing articles for a topic."""
    db = SessionLocal()
    
    try:
        # Get a topic from the database
        topic = db.query(Topic).first()
        
        if not topic:
            print("No topics found in the database. Please run the topic service test first.")
            return False
        
        print(f"\nAnalyzing articles for topic: {topic.name}")
        
        # Analyze articles for the topic
        result = article_analysis_service.analyze_articles_by_topic(db, topic.id, limit=5)
        
        # Print the results
        print("\nAnalysis results:")
        print(f"Topic ID: {result['topic_id']}")
        print(f"Articles found: {result.get('articles_found', 0)}")
        print(f"Articles analyzed: {result['articles_analyzed']}")
        print(f"Articles updated: {result['articles_updated']}")
        
        if result["errors"]:
            print("\nErrors:")
            for error in result["errors"]:
                print(f"- {error}")
        
        # Get articles with sentiment data for this topic
        from app.services.topic import topic_service
        articles = topic_service.get_topic_articles(db, topic.id, limit=5)
        
        print(f"\nArticles with sentiment data ({len(articles)}):")
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article.title}")
            print(f"   Source: {article.source_name}")
            print(f"   Sentiment: {article.sentiment_label} ({article.sentiment_score})")
            print(f"   Confidence: {article.sentiment_confidence}")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"Error in test: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("Testing article analysis...")
    
    # Test single article analysis
    success = test_analyze_article()
    
    if success:
        # Test topic articles analysis
        success = test_analyze_topic_articles()
    
    if success:
        print("\nTest completed!")
    else:
        print("\nTest failed.")