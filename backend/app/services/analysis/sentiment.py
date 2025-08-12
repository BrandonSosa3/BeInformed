"""
Sentiment Analysis Service

This module provides functionality to analyze the sentiment of text content,
specifically designed for article analysis.
"""

from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Set up logging
logger = logging.getLogger(__name__)

class SentimentAnalysisService:
    """Service for analyzing sentiment in text content using NLTK's VADER."""
    
    def __init__(self):
        """Initialize the sentiment analysis service."""
        self.is_initialized = False
        self.analyzer = None
    
    def initialize(self) -> bool:
        """
        Initialize the sentiment analysis resources.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        try:
            # Download VADER lexicon if not already downloaded
            try:
                nltk.data.find('sentiment/vader_lexicon.zip')
            except LookupError:
                logger.info("Downloading VADER lexicon...")
                nltk.download('vader_lexicon')
            
            # Initialize the VADER sentiment analyzer
            self.analyzer = SentimentIntensityAnalyzer()
            
            self.is_initialized = True
            logger.info("Sentiment analysis service initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize sentiment analysis service: {e}")
            return False
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of the provided text using VADER.
        
        Args:
            text (str): The text content to analyze
            
        Returns:
            Dict[str, Any]: A dictionary containing sentiment analysis results:
                - score: float between -1 (very negative) and 1 (very positive)
                - label: string label ("positive", "negative", "neutral")
                - confidence: float between 0 and 1 indicating confidence in the result
                - analysis_time: datetime when the analysis was performed
        """
        if not self.is_initialized:
            self.initialize()
        
        if not text or not text.strip():
            return {
                "score": 0.0,
                "label": "neutral",
                "confidence": 0.0,
                "analysis_time": datetime.now()
            }
        
        try:
            # Get sentiment scores using VADER
            scores = self.analyzer.polarity_scores(text)
            
            # The compound score is a normalized score between -1 and 1
            compound_score = scores['compound']
            
            # Determine label based on compound score
            if compound_score >= 0.05:
                label = "positive"
            elif compound_score <= -0.05:
                label = "negative"
            else:
                label = "neutral"
            
            # Calculate a confidence score based on the magnitude of the compound score
            # Higher absolute values indicate higher confidence
            confidence = min(abs(compound_score) * 1.5, 1.0)
            
            result = {
                "score": round(compound_score, 2),  # Round to 2 decimal places
                "label": label,
                "confidence": round(confidence, 2),
                "analysis_time": datetime.now()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            # Return a neutral result with low confidence in case of error
            return {
                "score": 0.0,
                "label": "neutral",
                "confidence": 0.0,
                "analysis_time": datetime.now()
            }
    
    def analyze_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the sentiment of an article.
        
        Args:
            article_data (Dict[str, Any]): Article data containing at least
                'title' and optionally 'description' and 'content'
                
        Returns:
            Dict[str, Any]: A dictionary containing sentiment analysis results
        """
        # Combine relevant fields for analysis, with higher weight to title
        text_parts = []
        
        if "title" in article_data and article_data["title"]:
            # Add title twice to give it more weight
            text_parts.append(article_data["title"])
            text_parts.append(article_data["title"])
            
        if "description" in article_data and article_data["description"]:
            text_parts.append(article_data["description"])
            
        if "content" in article_data and article_data["content"]:
            # Limit content to first 1000 chars to focus on the lead
            text_parts.append(article_data["content"][:1000])
        
        # If we have text to analyze, do the analysis
        if text_parts:
            text_to_analyze = " ".join(text_parts)
            return self.analyze_text(text_to_analyze)
        else:
            # Return neutral result if no text available
            return {
                "score": 0.0,
                "label": "neutral",
                "confidence": 0.0,
                "analysis_time": datetime.now()
            }
    
    def batch_analyze(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze sentiment for a batch of articles.
        
        Args:
            articles (List[Dict[str, Any]]): List of article data dictionaries
            
        Returns:
            List[Dict[str, Any]]: List of articles with sentiment analysis results added
        """
        results = []
        
        for article in articles:
            try:
                # Make a copy of the article to avoid modifying the original
                article_copy = article.copy()
                
                # Add sentiment analysis results
                article_copy["sentiment_analysis"] = self.analyze_article(article)
                
                results.append(article_copy)
            except Exception as e:
                logger.error(f"Error in batch analysis for article {article.get('id', 'unknown')}: {e}")
                # Add the original article without analysis
                results.append(article)
        
        return results

# Create a singleton instance for use throughout the application
sentiment_analysis_service = SentimentAnalysisService()