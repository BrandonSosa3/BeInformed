# Test script for integrated article analysis
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
    """Test analyzing a single article with integrated analysis."""
    db = SessionLocal()
    
    try:
        # Get an article from the database
        article = db.query(Article).first()
        
        if not article:
            print("No articles found in the database. Please run the article collection test first.")
            return False
        
        print(f"\nAnalyzing article: {article.title}")
        print(f"Source: {article.source_name}")
        
        # Check if the article already has analysis data
        if article.sentiment_score is not None or article.political_bias_score is not None:
            print(f"Article already has analysis data:")
            if article.sentiment_score is not None:
                print(f"  Sentiment: {article.sentiment_label} ({article.sentiment_score})")
            if article.political_bias_score is not None:
                print(f"  Political bias: {article.political_bias_label} ({article.political_bias_score})")
            if article.sensationalism_score is not None:
                print(f"  Sensationalism: {article.sensationalism_label} ({article.sensationalism_score})")
            print(f"  Last analyzed: {article.last_analyzed_at}")
        
        # Analyze the article
        result = article_analysis_service.analyze_article(article, db)
        
        # Print the results
        print("\nAnalysis results:")
        if result["sentiment"]:
            print(f"Sentiment score: {result['sentiment']['score']}")
            print(f"Sentiment label: {result['sentiment']['label']}")
            print(f"Confidence: {result['sentiment']['confidence']}")
        
        if result["bias"]:
            political_bias = result["bias"]["political_bias"]
            sensationalism = result["bias"]["sensationalism"]
            
            print(f"\nPolitical bias score: {political_bias['score']}")
            print(f"Political bias label: {political_bias['label']}")
            print(f"Political confidence: {political_bias['confidence']}")
            
            print(f"\nSensationalism score: {sensationalism['score']}")
            print(f"Sensationalism label: {sensationalism['label']}")
            print(f"Sensationalism confidence: {sensationalism['confidence']}")
        
        # Verify the database was updated
        db.refresh(article)
        print("\nArticle in database after analysis:")
        print(f"  Sentiment score: {article.sentiment_score}")
        print(f"  Sentiment label: {article.sentiment_label}")
        print(f"  Political bias score: {article.political_bias_score}")
        print(f"  Political bias label: {article.political_bias_label}")
        print(f"  Sensationalism score: {article.sensationalism_score}")
        print(f"  Sensationalism label: {article.sensationalism_label}")
        print(f"  Last analyzed: {article.last_analyzed_at}")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"Error in test: {e}")
        return False
    finally:
        db.close()

def test_analyze_topic_articles():
    """Test analyzing articles for a topic with integrated analysis."""
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
        
        # Get articles with analysis data for this topic
        from app.services.topic import topic_service
        articles = topic_service.get_topic_articles(db, topic.id, limit=5)
        
        print(f"\nArticles with analysis data ({len(articles)}):")
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article.title}")
            print(f"   Source: {article.source_name}")
            
            # Print sentiment data if available
            if article.sentiment_score is not None:
                print(f"   Sentiment: {article.sentiment_label} ({article.sentiment_score})")
            
            # Print political bias data if available
            if article.political_bias_score is not None:
                print(f"   Political bias: {article.political_bias_label} ({article.political_bias_score})")
            
            # Print sensationalism data if available
            if article.sensationalism_score is not None:
                print(f"   Sensationalism: {article.sensationalism_label} ({article.sensationalism_score})")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"Error in test: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("Testing integrated article analysis...")
    
    # Test single article analysis
    success = test_analyze_article()
    
    if success:
        # Test topic articles analysis
        success = test_analyze_topic_articles()
    
    if success:
        print("\nTest completed!")
    else:
        print("\nTest failed.")