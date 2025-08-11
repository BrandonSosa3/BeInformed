import os
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

class NewsAPIService:
    """Service for interacting with the NewsAPI."""
    
    BASE_URL = "https://newsapi.org/v2"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the NewsAPI service with an API key."""
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        if not self.api_key:
            raise ValueError("NewsAPI key is required. Set the NEWS_API_KEY environment variable.")
    
    def search_everything(
        self,
        query: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        language: str = "en",
        sort_by: str = "relevancy",
        page_size: int = 20,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search for articles matching the query across all sources.
        
        Args:
            query: Keywords or phrases to search for
            from_date: The oldest article allowed (default: 1 month ago)
            to_date: The newest article allowed (default: now)
            language: The language of the articles (default: English)
            sort_by: The order to sort articles (relevancy, popularity, publishedAt)
            page_size: Number of results per page (max 100)
            page: Page number
            
        Returns:
            Dict containing the search results
        """
        # Set default dates if not provided
        if not from_date:
            from_date = datetime.now() - timedelta(days=30)  # 1 month ago
        if not to_date:
            to_date = datetime.now()
        
        # Format dates as ISO strings
        from_str = from_date.strftime("%Y-%m-%d")
        to_str = to_date.strftime("%Y-%m-%d")
        
        # Prepare request parameters
        params = {
            "q": query,
            "from": from_str,
            "to": to_str,
            "language": language,
            "sortBy": sort_by,
            "pageSize": min(page_size, 100),  # Ensure we don't exceed API limits
            "page": page,
            "apiKey": self.api_key
        }
        
        # Make the request
        response = requests.get(f"{self.BASE_URL}/everything", params=params)
        
        # Check for errors
        response.raise_for_status()
        
        return response.json()
    
    def get_top_headlines(
        self,
        query: Optional[str] = None,
        country: Optional[str] = None,
        category: Optional[str] = None,
        page_size: int = 20,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Get top headlines based on query, country, or category.
        
        Args:
            query: Keywords or phrases to search for
            country: The 2-letter ISO 3166-1 code of the country (e.g., 'us', 'gb')
            category: Category of news (business, entertainment, health, etc.)
            page_size: Number of results per page (max 100)
            page: Page number
            
        Returns:
            Dict containing the top headlines
        """
        # At least one of query, country, or category must be specified
        if not any([query, country, category]):
            raise ValueError("At least one of query, country, or category must be specified")
        
        # Prepare request parameters
        params = {
            "pageSize": min(page_size, 100),
            "page": page,
            "apiKey": self.api_key
        }
        
        # Add optional parameters
        if query:
            params["q"] = query
        if country:
            params["country"] = country
        if category:
            params["category"] = category
        
        # Make the request
        response = requests.get(f"{self.BASE_URL}/top-headlines", params=params)
        
        # Check for errors
        response.raise_for_status()
        
        return response.json()
    
    def process_articles(self, articles_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process articles data from NewsAPI to a standardized format.
        
        Args:
            articles_data: Raw response from NewsAPI
            
        Returns:
            List of processed article dictionaries
        """
        if "articles" not in articles_data:
            return []
        
        processed_articles = []
        
        for article in articles_data["articles"]:
            # Skip articles with missing essential fields
            if not article.get("title") or not article.get("url"):
                continue
                
            processed_article = {
                "title": article.get("title"),
                "url": article.get("url"),
                "description": article.get("description"),
                "content": article.get("content"),
                "author": article.get("author"),
                "published_at": article.get("publishedAt"),
                "source_name": article.get("source", {}).get("name"),
                "source_url": None,  # NewsAPI doesn't provide source URL
                "image_url": article.get("urlToImage"),
                "metadata": {
                    "source_id": article.get("source", {}).get("id"),
                    "raw_data": article
                }
            }
            
            processed_articles.append(processed_article)
        
        return processed_articles

# Create a singleton instance for use throughout the application
news_api_service = NewsAPIService()