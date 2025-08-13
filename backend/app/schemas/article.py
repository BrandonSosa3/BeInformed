from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

# Article schemas
class ArticleBase(BaseModel):
    """Base schema for Article without ID."""
    title: str
    url: HttpUrl
    description: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    image_url: Optional[HttpUrl] = None
    source_name: Optional[str] = None

class ArticleCreate(ArticleBase):
    """Schema for creating a new Article."""
    source_id: Optional[int] = None

class ArticleUpdate(BaseModel):
    """Schema for updating an existing Article."""
    title: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    image_url: Optional[HttpUrl] = None
    source_id: Optional[int] = None
    source_name: Optional[str] = None
    credibility_score: Optional[float] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    sentiment_confidence: Optional[float] = None
    bias_scores: Optional[Dict[str, Any]] = None

class ArticleInDB(ArticleBase):
    """Schema for Article as stored in the database."""
    id: int
    source_id: Optional[int] = None
    credibility_score: Optional[float] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    sentiment_confidence: Optional[float] = None
    political_bias_score: Optional[float] = None
    political_bias_label: Optional[str] = None
    sensationalism_score: Optional[float] = None
    sensationalism_label: Optional[str] = None
    extractive_summary: Optional[str] = None
    beginner_summary: Optional[str] = None
    technical_summary: Optional[str] = None
    summary_generated_at: Optional[datetime] = None
    bias_scores: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_analyzed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Alias for the response model to make the API cleaner
Article = ArticleInDB

# Article list response
class ArticleList(BaseModel):
    """Schema for a list of articles with pagination info."""
    items: List[Article]
    total: int
    page: int
    size: int
    pages: int

    model_config = ConfigDict(from_attributes=True)