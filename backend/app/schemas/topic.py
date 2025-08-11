from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# Topic schemas
class TopicBase(BaseModel):
    """Base schema for Topic without ID."""
    name: str
    description: Optional[str] = None

class TopicCreate(TopicBase):
    """Schema for creating a new Topic."""
    pass

class TopicUpdate(BaseModel):
    """Schema for updating an existing Topic."""
    name: Optional[str] = None
    description: Optional[str] = None

class TopicInDB(TopicBase):
    """Schema for Topic as stored in the database."""
    id: int
    search_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_searched_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Alias for the response model to make the API cleaner
Topic = TopicInDB

# Topic search schemas
class TopicSearchRequest(BaseModel):
    """Schema for topic search request."""
    topic: str
    max_articles: Optional[int] = 20

class TopicSearchResponse(BaseModel):
    """Schema for topic search response."""
    topic: Topic
    is_new: bool
    articles_found: int
    articles_stored: int
    sources_found: int
    sources_stored: int
    errors: List[str] = []

    model_config = ConfigDict(from_attributes=True)