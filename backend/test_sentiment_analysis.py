# Test script for sentiment analysis service
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from app.services.analysis.sentiment import sentiment_analysis_service

def test_sentiment_analysis():
    """Test the sentiment analysis service with sample texts."""
    print("\nTesting Sentiment Analysis Service")
    print("==================================")
    
    # Test positive text
    positive_text = "I absolutely love this article! The writer did an amazing job explaining complex concepts in a clear and engaging way. This is definitely the best piece I've read this month."
    
    # Test negative text
    negative_text = "This article is terrible. The author clearly doesn't understand the topic and makes numerous factual errors. I wasted my time reading this poorly written piece."
    
    # Test neutral text
    neutral_text = "The article discusses various aspects of machine learning, including supervised and unsupervised learning techniques. It covers algorithms such as decision trees and neural networks."
    
    # Analyze the texts
    print("\nAnalyzing positive text...")
    positive_result = sentiment_analysis_service.analyze_text(positive_text)
    print(f"Result: {positive_result}")
    
    print("\nAnalyzing negative text...")
    negative_result = sentiment_analysis_service.analyze_text(negative_text)
    print(f"Result: {negative_result}")
    
    print("\nAnalyzing neutral text...")
    neutral_result = sentiment_analysis_service.analyze_text(neutral_text)
    print(f"Result: {neutral_result}")
    
    # Test article analysis
    print("\nTesting article analysis...")
    article = {
        "title": "Breakthrough in Renewable Energy Storage",
        "description": "Scientists develop new battery technology that could revolutionize renewable energy storage.",
        "content": "Researchers at MIT have announced a major breakthrough in battery technology that could solve one of the biggest challenges in renewable energy adoption. The new battery design can store energy for months with minimal loss, potentially making solar and wind power more reliable and cost-effective. 'This is a game-changer for the renewable energy industry,' said Dr. Emily Chen, lead researcher on the project."
    }
    
    article_result = sentiment_analysis_service.analyze_article(article)
    print(f"Article sentiment: {article_result}")
    
    return True

if __name__ == "__main__":
    test_sentiment_analysis()