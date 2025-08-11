from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class Source(Base):
    """
    Database model for information sources.
    
    This represents external content sources like news articles,
    academic papers, social media posts, etc.
    """
    # Tell SQLAlchemy what table this model maps to
    __tablename__ = "sources"
    
    # Define columns
    # Primary key - unique identifier for each row
    id = Column(Integer, primary_key=True, index=True)
    
    # URL of the source - must be unique
    url = Column(String, unique=True, index=True)
    
    # Title of the source
    title = Column(String)
    
    # Description or summary
    description = Column(Text, nullable=True)  # nullable=True means this field can be empty
    
    # Type of source (news, academic, social media, etc.)
    source_type = Column(String)
    
    # When this record was created (automatically set)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # When this record was last updated (automatically updated)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Credibility score (calculated by our AI)
    credibility_score = Column(Float, nullable=True)
    
    articles = relationship("Article", back_populates="source")

    def __repr__(self):
        """String representation of this object"""
        return f"<Source {self.title}>"