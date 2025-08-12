# Test script for bias detection service
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath('.'))

from app.services.analysis.bias import bias_detection_service

def test_bias_detection():
    """Test the bias detection service with sample texts."""
    print("\nTesting Bias Detection Service")
    print("===============================")
    
    # Test left-leaning text
    left_leaning_text = """
    Progressive policies are needed to address systemic racism and income inequality in our society.
    Universal healthcare should be a fundamental right for all citizens, and the government must take
    action on climate crisis immediately. We need to protect reproductive rights and implement
    common-sense gun control measures. The Green New Deal offers a path forward to a more equitable future.
    """
    
    # Test right-leaning text
    right_leaning_text = """
    Conservative values and traditional family values are the backbone of our society. 
    We need smaller government and lower taxes to stimulate economic growth through the free market.
    Protecting religious freedom and Second Amendment rights must be a priority, along with
    strong border security measures to ensure national security and law and order.
    """
    
    # Test neutral political text
    neutral_text = """
    The legislation was passed by Congress yesterday with support from both parties.
    Representatives will vote on the policy next week after the senate reviews the proposal.
    The government has published new regulations regarding the implementation of the law.
    """
    
    # Test sensationalist text
    sensationalist_text = """
    SHOCKING BOMBSHELL report reveals the HORRIFIC and DEVASTATING scandal that has erupted into
    ABSOLUTE CHAOS! This MIND-BLOWING crisis has created a NIGHTMARE scenario that will
    completely DESTROY everything you thought you knew! You won't believe what happens next in this
    JAW-DROPPING catastrophe - the worst disaster ever seen!
    """
    
    # Test factual text
    factual_text = """
    The report indicates that economic growth slowed to 2.3% in the third quarter, 
    which represents a decrease from the previous quarter's 2.8% growth. Analysts attribute
    this change to several factors, including rising interest rates and decreased consumer spending
    in certain sectors. The data suggests a potential trend that will require further monitoring.
    """
    
    # Analyze the texts for political bias
    print("\nAnalyzing left-leaning text for political bias...")
    left_result = bias_detection_service.detect_political_bias(left_leaning_text)
    print(f"Political bias score: {left_result['score']} ({left_result['label']})")
    print(f"Confidence: {left_result['confidence']}")
    print(f"Left-leaning matches: {len(left_result['matches']['left'])}")
    print(f"Right-leaning matches: {len(left_result['matches']['right'])}")
    
    print("\nAnalyzing right-leaning text for political bias...")
    right_result = bias_detection_service.detect_political_bias(right_leaning_text)
    print(f"Political bias score: {right_result['score']} ({right_result['label']})")
    print(f"Confidence: {right_result['confidence']}")
    print(f"Left-leaning matches: {len(right_result['matches']['left'])}")
    print(f"Right-leaning matches: {len(right_result['matches']['right'])}")
    
    print("\nAnalyzing neutral text for political bias...")
    neutral_result = bias_detection_service.detect_political_bias(neutral_text)
    print(f"Political bias score: {neutral_result['score']} ({neutral_result['label']})")
    print(f"Confidence: {neutral_result['confidence']}")
    
    # Analyze the texts for sensationalism
    print("\nAnalyzing sensationalist text...")
    sensational_result = bias_detection_service.detect_sensationalism(sensationalist_text)
    print(f"Sensationalism score: {sensational_result['score']} ({sensational_result['label']})")
    print(f"Confidence: {sensational_result['confidence']}")
    print(f"Sensationalist matches: {len(sensational_result['matches'])}")
    
    print("\nAnalyzing factual text...")
    factual_result = bias_detection_service.detect_sensationalism(factual_text)
    print(f"Sensationalism score: {factual_result['score']} ({factual_result['label']})")
    print(f"Confidence: {factual_result['confidence']}")
    
    # Test the comprehensive article analysis
    print("\nTesting comprehensive article analysis...")
    article = {
        "title": "Progressive Policies Cause Economic Chaos as Markets Crash",
        "description": "The shocking impact of liberal policies on the free market economy has created a devastating scenario for businesses.",
        "content": "Conservative analysts argue that the government's interference in the market through regulations and higher taxes has stifled growth and innovation. The catastrophic results can be seen in recent economic indicators, which show a significant downturn in key sectors. Business leaders are calling for a return to traditional economic principles and smaller government to restore stability and growth."
    }
    
    article_result = bias_detection_service.analyze_article(article)
    print("\nArticle analysis results:")
    print(f"Political bias: {article_result['political_bias']['score']} ({article_result['political_bias']['label']})")
    print(f"Political confidence: {article_result['political_bias']['confidence']}")
    print(f"Sensationalism: {article_result['sensationalism']['score']} ({article_result['sensationalism']['label']})")
    print(f"Sensationalism confidence: {article_result['sensationalism']['confidence']}")
    
    return True

if __name__ == "__main__":
    test_bias_detection()