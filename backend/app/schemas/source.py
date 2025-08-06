from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class SourceBase(BaseModel):
    """Base schema for Source without ID."""
    url: HttpUrl
    title: str
    description: Optional[str] = None
    source_type: str

class SourceCreate(SourceBase):
    """Schema for creating a new Source."""
    pass

class SourceUpdate(BaseModel):
    """Schema for updating an existing Source."""
    url: Optional[HttpUrl] = None
    title: Optional[str] = None
    description: Optional[str] = None
    source_type: Optional[str] = None
    credibility_score: Optional[float] = None

class SourceInDB(SourceBase):
    """Schema for Source as stored in the database."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    credibility_score: Optional[float] = None

    class Config:
        orm_mode = True

# Alias for the response model to make the API cleaner
Source = SourceInDB
