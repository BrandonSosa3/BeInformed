"""
Bias Detection Service

This module provides functionality to analyze the political bias and
sensationalism of text content, specifically designed for article analysis.
"""

from typing import Dict, Any, List, Optional, Tuple
import logging
import re
from datetime import datetime
import string

from app.data.bias_lexicons import (
    LEFT_LEANING_TERMS,
    RIGHT_LEANING_TERMS,
    SENSATIONALIST_TERMS,
    NEUTRAL_POLITICAL_TERMS
)

# Set up logging
logger = logging.getLogger(__name__)

class BiasDetectionService:
    """Service for analyzing political bias and sensationalism in text content."""
    
    def __init__(self):
        """Initialize the bias detection service."""
        self.is_initialized = False
        self.left_terms = LEFT_LEANING_TERMS
        self.right_terms = RIGHT_LEANING_TERMS
        self.sensationalist_terms = SENSATIONALIST_TERMS
        self.neutral_terms = NEUTRAL_POLITICAL_TERMS
    
    def initialize(self) -> bool:
        """
        Initialize the bias detection resources.
        
        Returns:
            bool: True if initialization was successful, False otherwise
        """
        try:
            # Compile the terms into lowercase for case-insensitive matching
            self._compile_terms()
            
            self.is_initialized = True
            logger.info("Bias detection service initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize bias detection service: {e}")
            return False
    
    def _compile_terms(self):
        """Preprocess and compile the term dictionaries for efficient matching."""
        # Ensure all keys are lowercase
        self.left_terms = {k.lower(): v for k, v in self.left_terms.items()}
        self.right_terms = {k.lower(): v for k, v in self.right_terms.items()}
        self.sensationalist_terms = {k.lower(): v for k, v in self.sensationalist_terms.items()}
        self.neutral_terms = {k.lower(): v for k, v in self.neutral_terms.items()}
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for analysis.
        
        Args:
            text: The text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation that might interfere with word matching
        # but preserve hyphens and apostrophes for compound words and contractions
        for p in string.punctuation.replace('-', '').replace("'", ""):
            text = text.replace(p, ' ')
            
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def detect_political_bias(self, text: str) -> Dict[str, Any]:
        """
        Detect political bias in the provided text.
        
        Args:
            text: The text content to analyze
            
        Returns:
            Dict containing political bias analysis results:
                - score: float between -1.0 (far left) and 1.0 (far right)
                - label: string label for the political leaning
                - confidence: float between 0 and 1 indicating confidence
                - matches: dictionary of matched terms and their counts
        """
        if not self.is_initialized:
            self.initialize()
        
        if not text or not text.strip():
            return {
                "score": 0.0,
                "label": "neutral",
                "confidence": 0.0,
                "matches": {}
            }
        
        try:
            # Preprocess the text
            processed_text = self._preprocess_text(text)
            
            # Count occurrences and calculate scores
            left_matches = {}
            right_matches = {}
            neutral_matches = {}
            
            # Check for each left-leaning term
            for term, weight in self.left_terms.items():
                count = processed_text.count(term)
                if count > 0:
                    left_matches[term] = {"count": count, "weight": weight}
            
            # Check for each right-leaning term
            for term, weight in self.right_terms.items():
                count = processed_text.count(term)
                if count > 0:
                    right_matches[term] = {"count": count, "weight": weight}
            
            # Check for each neutral term
            for term, weight in self.neutral_terms.items():
                count = processed_text.count(term)
                if count > 0:
                    neutral_matches[term] = {"count": count, "weight": weight}
            
            # Calculate weighted scores
            left_score = sum(item["count"] * item["weight"] for item in left_matches.values())
            right_score = sum(item["count"] * item["weight"] for item in right_matches.values())
            neutral_score = sum(item["count"] * item["weight"] for item in neutral_matches.values())
            
            # Calculate political bias score (-1 to 1, left to right)
            total_weight = left_score + right_score
            
            if total_weight == 0:
                political_score = 0.0
                confidence = 0.0
            else:
                # Calculate bias score: negative for left, positive for right
                political_score = (right_score - left_score) / (right_score + left_score)
                
                # Calculate confidence based on total matched terms and their weights
                # compared to neutral terms
                total_matched_terms = len(left_matches) + len(right_matches)
                total_political_weight = left_score + right_score
                total_all_weight = total_political_weight + neutral_score
                
                if total_all_weight == 0:
                    confidence = 0.0
                else:
                    # Higher confidence when more political terms are found
                    # and when the ratio of political to neutral terms is higher
                    confidence = min(
                        (total_matched_terms / 10) * (total_political_weight / (total_all_weight + 0.1)),
                        1.0
                    )
            
            # Round the score and confidence to 2 decimal places
            political_score = round(political_score, 2)
            confidence = round(confidence, 2)
            
            # Determine the label based on the score
            if political_score < -0.3:
                label = "left-leaning"
            elif political_score > 0.3:
                label = "right-leaning"
            else:
                label = "centrist"
            
            # If confidence is very low, label as neutral
            if confidence < 0.2:
                label = "neutral"
                political_score = 0.0
            
            # Prepare the matches dictionary for return
            all_matches = {
                "left": left_matches,
                "right": right_matches,
                "neutral": neutral_matches
            }
            
            return {
                "score": political_score,
                "label": label,
                "confidence": confidence,
                "matches": all_matches
            }
            
        except Exception as e:
            logger.error(f"Error detecting political bias: {e}")
            return {
                "score": 0.0,
                "label": "neutral",
                "confidence": 0.0,
                "matches": {}
            }
    
    def detect_sensationalism(self, text: str) -> Dict[str, Any]:
        """
        Detect sensationalism in the provided text.
        
        Args:
            text: The text content to analyze
            
        Returns:
            Dict containing sensationalism analysis results:
                - score: float between 0.0 (factual) and 1.0 (sensational)
                - label: string label for the sensationalism level
                - confidence: float between 0 and 1 indicating confidence
                - matches: dictionary of matched terms and their counts
        """
        if not self.is_initialized:
            self.initialize()
        
        if not text or not text.strip():
            return {
                "score": 0.0,
                "label": "factual",
                "confidence": 0.0,
                "matches": {}
            }
        
        try:
            # Preprocess the text
            processed_text = self._preprocess_text(text)
            
            # Count occurrences and calculate scores
            sensational_matches = {}
            
            # Check for each sensationalist term
            for term, weight in self.sensationalist_terms.items():
                count = processed_text.count(term)
                if count > 0:
                    sensational_matches[term] = {"count": count, "weight": weight}
            
            # Calculate weighted score
            sensational_score = sum(item["count"] * item["weight"] for item in sensational_matches.values())
            
            # Normalize the score to range 0-1
            # The formula below assumes that a typical sensational article might have around 10-15 weighted matches
            # We cap at 1.0 to avoid scores above 1
            normalized_score = min(sensational_score / 10.0, 1.0)
            
            # Calculate confidence based on the number of matched terms
            confidence = min(len(sensational_matches) / 8.0, 1.0)
            
            # Round the scores to 2 decimal places
            normalized_score = round(normalized_score, 2)
            confidence = round(confidence, 2)
            
            # Determine the label based on the score
            if normalized_score < 0.3:
                label = "factual"
            elif normalized_score < 0.6:
                label = "somewhat sensational"
            else:
                label = "highly sensational"
            
            return {
                "score": normalized_score,
                "label": label,
                "confidence": confidence,
                "matches": sensational_matches
            }
            
        except Exception as e:
            logger.error(f"Error detecting sensationalism: {e}")
            return {
                "score": 0.0,
                "label": "factual",
                "confidence": 0.0,
                "matches": {}
            }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive bias analysis on the provided text.
        
        Args:
            text: The text content to analyze
            
        Returns:
            Dict containing bias analysis results including political bias and sensationalism
        """
        if not self.is_initialized:
            self.initialize()
        
        political_bias = self.detect_political_bias(text)
        sensationalism = self.detect_sensationalism(text)
        
        return {
            "political_bias": political_bias,
            "sensationalism": sensationalism,
            "analysis_time": datetime.now()
        }
    
    def analyze_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the bias in an article.
        
        Args:
            article_data: Article data containing at least
                'title' and optionally 'description' and 'content'
                
        Returns:
            Dict containing bias analysis results
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
            text_parts.append(article_data["content"])
        
        # If we have text to analyze, do the analysis
        if text_parts:
            text_to_analyze = " ".join(text_parts)
            return self.analyze_text(text_to_analyze)
        else:
            # Return neutral result if no text available
            return {
                "political_bias": {
                    "score": 0.0,
                    "label": "neutral",
                    "confidence": 0.0,
                    "matches": {}
                },
                "sensationalism": {
                    "score": 0.0,
                    "label": "factual",
                    "confidence": 0.0,
                    "matches": {}
                },
                "analysis_time": datetime.now()
            }

# Create a singleton instance for use throughout the application
bias_detection_service = BiasDetectionService()