# Test script for NewsAPI service
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from app.services.external.news_api import news_api_service

def test_search_everything():
    """Test the search_everything method."""
    try:
        # Search for articles about AI
        results = news_api_service.search_everything(
            query="artificial intelligence",
            page_size=5  # Limit to 5 results to save API calls
        )
        
        # Print the results
        print(f"Found {results.get('totalResults', 0)} articles about AI")
        
        # Process the articles
        processed_articles = news_api_service.process_articles(results)
        
        # Print the processed articles
        for i, article in enumerate(processed_articles, 1):
            print(f"\nArticle {i}:")
            print(f"Title: {article['title']}")
            print(f"Source: {article['source_name']}")
            print(f"URL: {article['url']}")
            print(f"Published: {article['published_at']}")
            print(f"Description: {article['description'][:100]}..." if article['description'] else "No description")
        
        return True
    except Exception as e:
        print(f"Error testing search_everything: {e}")
        return False

def test_get_top_headlines():
    """Test the get_top_headlines method."""
    try:
        # Get top headlines for technology
        results = news_api_service.get_top_headlines(
            category="technology",
            country="us",
            page_size=5  # Limit to 5 results to save API calls
        )
        
        # Print the results
        print(f"\nFound {results.get('totalResults', 0)} top headlines for technology")
        
        # Process the articles
        processed_articles = news_api_service.process_articles(results)
        
        # Print the processed articles
        for i, article in enumerate(processed_articles, 1):
            print(f"\nHeadline {i}:")
            print(f"Title: {article['title']}")
            print(f"Source: {article['source_name']}")
            print(f"URL: {article['url']}")
            print(f"Published: {article['published_at']}")
        
        return True
    except Exception as e:
        print(f"Error testing get_top_headlines: {e}")
        return False

if __name__ == "__main__":
    print("Testing NewsAPI Service...")
    
    search_success = test_search_everything()
    headlines_success = test_get_top_headlines()
    
    if search_success and headlines_success:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed.")