"""
Summarization Service

This module provides functionality to generate summaries of article content,
including extractive summarization and text simplification.
"""

from typing import Dict, Any, List, Optional, Union
import logging
import re
import math
import string
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

class SummarizationService:
    """Service for generating article summaries."""
    
    def __init__(self):
        """Initialize the summarization service."""
        self.is_initialized = True
        self.stop_words = {
            'a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'on', 'at', 'to', 'by', 'in',
            'of', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'having', 'do', 'does', 'did', 'doing', 'it', 'its', 'it\'s', 'that', 'they',
            'them', 'their', 'this', 'these', 'those', 'with', 'as', 'from', 'about', 'into'
        }
        
        # Technical terminology dictionary with simpler alternatives
        self.technical_terms = {
            'algorithm': 'step-by-step process',
            'artificial intelligence': 'computer systems that can perform tasks that normally need human intelligence',
            'machine learning': 'computers learning from data',
            'neural network': 'computer system inspired by the human brain',
            'deep learning': 'advanced machine learning technique',
            'natural language processing': 'computers understanding human language',
            'computer vision': 'computers understanding images and videos',
            'data mining': 'finding patterns in large datasets',
            'blockchain': 'secure digital record-keeping system',
            'cryptocurrency': 'digital currency',
            'encryption': 'secure coding of information',
            'quantum computing': 'advanced computing using quantum physics',
            'augmented reality': 'technology that adds digital elements to the real world',
            'virtual reality': 'computer-generated simulation of a 3D environment',
            'cloud computing': 'using remote servers over the internet',
            'internet of things': 'everyday devices connected to the internet',
            'big data': 'extremely large data sets',
            'cybersecurity': 'protecting computer systems from attacks',
            'bandwidth': 'data transfer capacity',
            'biometrics': 'body measurements used for identification',
            'api': 'way for different software to communicate',
            'protocol': 'set of rules for data exchange',
            'serverless': 'cloud computing without managing servers',
            'microservices': 'small, independent services that make up an application',
            'containerization': 'packaging software code with everything it needs to run',
            'devops': 'combining software development and IT operations',
            'firmware': 'software programmed into a device',
            'middleware': 'software that connects different applications',
            'sdk': 'set of tools for creating software',
            'saas': 'software provided as a service over the internet'
        }
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text for summarization.
        
        Args:
            text: The text to preprocess
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        
        return text.strip()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using simple rules.
        
        Args:
            text: The text to split
            
        Returns:
            List of sentences
        """
        # Simple sentence splitting using regex
        # This handles periods, question marks, and exclamation points as sentence boundaries
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        
        # Filter out very short sentences (likely not useful for summary)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        return sentences
    
    def _split_into_words(self, text: str) -> List[str]:
        """
        Split text into words using simple rules.
        
        Args:
            text: The text to split
            
        Returns:
            List of words
        """
        # Convert to lowercase and remove punctuation
        text = text.lower()
        for p in string.punctuation:
            text = text.replace(p, ' ')
        
        # Split by whitespace
        words = text.split()
        
        return words
    
    def _calculate_word_frequencies(self, text: str) -> Dict[str, int]:
        """
        Calculate the frequency of each word in the text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary of word frequencies
        """
        # Get words from text
        words = self._split_into_words(text)
        
        # Remove stop words
        words = [word for word in words if word not in self.stop_words]
        
        # Calculate word frequencies
        word_frequencies = {}
        for word in words:
            if word in word_frequencies:
                word_frequencies[word] += 1
            else:
                word_frequencies[word] = 1
        
        # Normalize frequencies
        max_frequency = max(word_frequencies.values()) if word_frequencies else 1
        for word in word_frequencies:
            word_frequencies[word] = word_frequencies[word] / max_frequency
        
        return word_frequencies
    
    def _score_sentences(self, sentences: List[str], word_frequencies: Dict[str, int]) -> Dict[str, float]:
        """
        Score sentences based on word frequencies and position.
        
        Args:
            sentences: List of sentences
            word_frequencies: Dictionary of word frequencies
            
        Returns:
            Dictionary of sentence scores
        """
        sentence_scores = {}
        
        # Weight for position importance (first and last paragraphs)
        first_quarter = max(1, len(sentences) // 4)
        last_quarter = max(1, len(sentences) // 4)
        
        for i, sentence in enumerate(sentences):
            # Initialize score
            if sentence not in sentence_scores:
                sentence_scores[sentence] = 0
                
            # Score based on word frequencies
            words = self._split_into_words(sentence)
            for word in words:
                if word in word_frequencies:
                    sentence_scores[sentence] += word_frequencies[word]
            
            # Normalize by sentence length to avoid favoring very long sentences
            if len(words) > 0:
                sentence_scores[sentence] = sentence_scores[sentence] / len(words)
            
            # Give bonus to sentences in the first and last quarter (introduction and conclusion)
            position_multiplier = 1.0
            if i < first_quarter:
                position_multiplier = 1.25  # 25% bonus for early sentences
            elif i >= len(sentences) - last_quarter:
                position_multiplier = 1.15  # 15% bonus for concluding sentences
            
            sentence_scores[sentence] *= position_multiplier
            
            # Favor sentences with question marks for engaging summaries
            if '?' in sentence:
                sentence_scores[sentence] *= 1.2
        
        return sentence_scores
    
    def generate_extractive_summary(
        self, 
        text: str, 
        max_sentences: int = 5,
        min_sentences: int = 2,
        prefer_start: bool = False
    ) -> str:
        """
        Generate an extractive summary by selecting the most important sentences.
        
        Args:
            text: The text to summarize
            max_sentences: Maximum number of sentences to include
            min_sentences: Minimum number of sentences to include
            prefer_start: Whether to prefer sentences from the beginning of the text
            
        Returns:
            Extractive summary
        """
        if not text or not text.strip():
            return ""
        
        try:
            # Preprocess the text
            preprocessed_text = self._preprocess_text(text)
            
            # Split the text into sentences
            sentences = self._split_into_sentences(preprocessed_text)
            
            # If text is very short, return it as is
            if len(sentences) <= min_sentences:
                return text
            
            # Calculate word frequencies
            word_frequencies = self._calculate_word_frequencies(preprocessed_text)
            
            # Score sentences
            sentence_scores = self._score_sentences(sentences, word_frequencies)
            
            # Determine number of sentences for the summary
            num_sentences = min(max_sentences, max(min_sentences, len(sentences) // 3))
            
            # If we prefer sentences from the start (for beginner summaries)
            if prefer_start and len(sentences) > 0:
                # Always include the first sentence (often contains the main point)
                first_sentence = sentences[0]
                sentence_scores[first_sentence] *= 1.5  # Boost its score
            
            # Select top sentences
            top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
            
            # Get original positions of selected sentences
            selected_sentences = [sentence for sentence, score in top_sentences]
            original_positions = [i for i, s in enumerate(sentences) if s in selected_sentences]
            
            # Sort by original position to maintain flow
            ordered_sentences = [sentences[i] for i in sorted(original_positions)]
            
            # Join sentences to create the summary
            summary = " ".join(ordered_sentences)
            
            return summary
        
        except Exception as e:
            logger.error(f"Error generating extractive summary: {e}")
            return ""
    
    def simplify_sentence(self, sentence: str) -> str:
        """
        Simplify a sentence by replacing technical terms and shortening.
        
        Args:
            sentence: The sentence to simplify
            
        Returns:
            Simplified sentence
        """
        simplified = sentence.lower()
        
        # Replace technical terms with simpler alternatives
        for term, simple_term in self.technical_terms.items():
            # Use word boundaries to avoid partial replacements
            pattern = r'\b' + re.escape(term) + r'\b'
            simplified = re.sub(pattern, simple_term, simplified, flags=re.IGNORECASE)
        
        # Shorten very long sentences
        words = simplified.split()
        if len(words) > 20:
            # Find a good breaking point (preposition or conjunction) around the middle
            breaking_points = ['and', 'but', 'or', 'so', 'because', 'as', 'since', 
                               'although', 'though', 'while', 'whereas', 'if', 'unless',
                               'until', 'when', 'where', 'which', 'who', 'that', 'whose']
            
            # Look for breaking points near the middle
            mid_point = len(words) // 2
            for i in range(mid_point - 3, mid_point + 4):
                if 0 <= i < len(words) and words[i].lower() in breaking_points:
                    return " ".join(words[:i+1]) + "."
            
            # If no good breaking point, just take the first part
            return " ".join(words[:15]) + "."
        
        # Capitalize first letter
        if simplified and len(simplified) > 0:
            simplified = simplified[0].upper() + simplified[1:]
        
        return simplified
    
    def generate_beginner_summary(self, text: str, max_words: int = 150) -> str:
        """
        Generate a beginner-friendly summary with simplified language.
        
        Args:
            text: The text to summarize
            max_words: Maximum number of words for the summary
            
        Returns:
            Beginner-friendly summary
        """
        try:
            # First, generate an extractive summary with preference for introductory sentences
            extractive_summary = self.generate_extractive_summary(
                text, 
                max_sentences=3,  # Shorter for beginners
                prefer_start=True  # Prefer introductory sentences
            )
            
            # Split into sentences for simplification
            sentences = self._split_into_sentences(extractive_summary)
            
            # Simplify each sentence
            simplified_sentences = [self.simplify_sentence(s) for s in sentences]
            
            # Join simplified sentences
            simplified_summary = " ".join(simplified_sentences)
            
            # Limit to max words
            words = simplified_summary.split()
            if len(words) > max_words:
                simplified_summary = " ".join(words[:max_words]) + "..."
            
            return simplified_summary
        
        except Exception as e:
            logger.error(f"Error generating beginner summary: {e}")
            return ""
    
    def identify_technical_terms(self, text: str) -> List[str]:
        """
        Identify technical terms in the text.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of technical terms found
        """
        found_terms = []
        
        # Look for technical terms in the text
        for term in self.technical_terms.keys():
            pattern = r'\b' + re.escape(term) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                found_terms.append(term)
        
        return found_terms
    
    def generate_technical_summary(self, text: str, max_words: int = 300) -> str:
        """
        Generate a more detailed technical summary that preserves technical terms.
        
        Args:
            text: The text to summarize
            max_words: Maximum number of words for the summary
            
        Returns:
            Technical summary
        """
        try:
            # First, identify technical terms in the full text
            technical_terms = self.identify_technical_terms(text)
            
            # Generate a longer extractive summary
            extractive_summary = self.generate_extractive_summary(
                text, 
                max_sentences=6  # More comprehensive for technical readers
            )
            
            # Make sure all sentences with technical terms are included
            sentences = self._split_into_sentences(text)
            summary_sentences = self._split_into_sentences(extractive_summary)
            
            # Find sentences with technical terms that aren't in the summary
            for term in technical_terms:
                if any(term.lower() in s.lower() for s in summary_sentences):
                    continue  # Term is already covered
                    
                # Find a sentence with this term to add
                for sentence in sentences:
                    if term.lower() in sentence.lower() and sentence not in summary_sentences:
                        summary_sentences.append(sentence)
                        break
            
            # Limit to reasonable length
            if len(summary_sentences) > 8:
                summary_sentences = summary_sentences[:8]
                
            # Sort by original position
            original_positions = []
            for s in summary_sentences:
                try:
                    original_positions.append(sentences.index(s))
                except ValueError:
                    # If not found, add to the end
                    original_positions.append(len(sentences))
            
            # Sort sentences by their original order
            ordered_sentences = [s for _, s in sorted(zip(original_positions, summary_sentences))]
            
            # Join sentences to create the summary
            technical_summary = " ".join(ordered_sentences)
            
            # Limit to max words
            words = technical_summary.split()
            if len(words) > max_words:
                technical_summary = " ".join(words[:max_words]) + "..."
            
            return technical_summary
        
        except Exception as e:
            logger.error(f"Error generating technical summary: {e}")
            return ""
    
    def summarize_article(self, article_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate summaries for an article.
        
        Args:
            article_data: Article data containing at least
                'title' and optionally 'description' and 'content'
                
        Returns:
            Dict containing different summary types
        """
        # Combine article content for summarization
        text_to_summarize = ""
        
        if "title" in article_data and article_data["title"]:
            text_to_summarize += article_data["title"] + ". "
            
        if "description" in article_data and article_data["description"]:
            text_to_summarize += article_data["description"] + " "
            
        if "content" in article_data and article_data["content"]:
            text_to_summarize += article_data["content"]
        
        # If we have text to summarize, generate summaries
        if text_to_summarize:
            try:
                extractive_summary = self.generate_extractive_summary(text_to_summarize)
                beginner_summary = self.generate_beginner_summary(text_to_summarize)
                technical_summary = self.generate_technical_summary(text_to_summarize)
                
                return {
                    "extractive": extractive_summary,
                    "beginner": beginner_summary,
                    "technical": technical_summary
                }
            except Exception as e:
                logger.error(f"Error summarizing article: {e}")
                return {
                    "extractive": "",
                    "beginner": "",
                    "technical": ""
                }
        else:
            # Return empty summaries if no text available
            return {
                "extractive": "",
                "beginner": "",
                "technical": ""
            }

# Create a singleton instance for use throughout the application
summarization_service = SummarizationService()