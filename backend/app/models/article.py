from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.db.base import Base

class Article(Base):
    """
    Database model for articles collected from various sources.
    """
    __tablename__ = "articles"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Article content and metadata
    title = Column(String, nullable=False, index=True)
    url = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    author = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)
    image_url = Column(String, nullable=True)
    
    # Source information
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    source = relationship("Source", back_populates="articles")
    source_name = Column(String, nullable=True)  # For cases where we don't have a source in our DB
    
    # Analysis metadata
    credibility_score = Column(Float, nullable=True)
    sentiment_score = Column(Float, nullable=True)  # -1 to 1, negative to positive
    bias_scores = Column(JSON, nullable=True)  # Stores various bias dimensions as JSON
    
    # System metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_analyzed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    topic_articles = relationship("TopicArticle", back_populates="article", cascade="all, delete-orphan", overlaps="topics")
    topics = relationship("Topic", secondary="topic_articles", back_populates="articles", overlaps="topic_articles, article")

    sentiment_score = Column(Float, nullable=True, index=True, comment="Sentiment score from -1 (negative) to 1 (positive)")
    sentiment_label = Column(String(20), nullable=True, comment="Sentiment label (positive, negative, neutral)")
    sentiment_confidence = Column(Float, nullable=True, comment="Confidence score for sentiment analysis (0-1)")

    political_bias_score = Column(Float, nullable=True, comment="Political bias score from -1.0 (far left) to 1.0 (far right)")
    political_bias_label = Column(String(50), nullable=True, comment="Political bias")
    # Add only these new fields to the Article class in app/models/article.py
    sensationalism_score = Column(Float, nullable=True, index=True, comment="Sensationalism score from 0.0 (objective) to 1.0 (sensationalist)")
    sensationalism_label = Column(String(20), nullable=True, comment="Sensationalism label (factual, somewhat sensational, highly sensational)")
    
    def __repr__(self):
        return f"<Article {self.id}: {self.title}>"