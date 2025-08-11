from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

# Association table for many-to-many relationship between topics and articles
class TopicArticle(Base):
    """Association table for the many-to-many relationship between topics and articles."""
    __tablename__ = "topic_articles"
    
    topic_id = Column(Integer, ForeignKey("topics.id"), primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    relevance_score = Column(Integer, nullable=True)  # Optional relevance score
    
    # Relationships
    topic = relationship("Topic", back_populates="topic_articles", overlaps="articles")
    article = relationship("Article", back_populates="topic_articles", overlaps="topics")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Topic(Base):
    """
    Database model for topics that users can search for.
    """
    __tablename__ = "topics"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Topic information
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    # Metadata
    search_count = Column(Integer, default=0)  # How many times this topic has been searched
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_searched_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    topic_articles = relationship("TopicArticle", back_populates="topic", cascade="all, delete-orphan")
    articles = relationship("Article", secondary="topic_articles", back_populates="topics", overlaps="topic_articles, topic")
    
    def __repr__(self):
        return f"<Topic {self.id}: {self.name}>"