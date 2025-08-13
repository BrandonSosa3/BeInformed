# Test script for article analysis with summaries
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

def test_analyze_article_with_summaries():
    """Test analyzing an article with summary generation."""
    db = SessionLocal()
    
    try:
        # Get an article from the database
        article = db.query(Article).first()
        
        if not article:
            print("No articles found in the database. Please run the article collection test first.")
            return False
        
        print(f"\nAnalyzing article: {article.title}")
        print(f"Source: {article.source_name}")
        
        # Check if the article already has summaries
        if article.extractive_summary:
            print(f"Article already has summaries:")
            print(f"  Extractive summary: {article.extractive_summary[:100]}...")
            print(f"  Beginner summary: {article.beginner_summary[:100]}...")
            print(f"  Technical summary: {article.technical_summary[:100]}...")
            print(f"  Generated at: {article.summary_generated_at}")
        
        # Analyze the article
        result = article_analysis_service.analyze_article(article, db)
        
        # Print the results
        print("\nAnalysis results:")
        
        if result["summaries"]:
            print("\nSummaries:")
            print(f"Extractive: {result['summaries']['extractive']}")
            print(f"Beginner: {result['summaries']['beginner']}")
            print(f"Technical: {result['summaries']['technical']}")
        
        # Verify the database was updated
        db.refresh(article)
        print("\nArticle in database after analysis:")
        print(f"  Extractive summary: {article.extractive_summary}")
        print(f"  Beginner summary: {article.beginner_summary}")
        print(f"  Technical summary: {article.technical_summary}")
        print(f"  Summary generated at: {article.summary_generated_at}")
        
        return True
    except Exception as e:
        db.rollback()
        print(f"Error in test: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("Testing article analysis with summaries...")
    
    success = test_analyze_article_with_summaries()
    
    if success:
        print("\nTest completed!")
    else:
        print("\nTest failed.")