from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.source import Source
from app.schemas.source import SourceCreate, SourceUpdate

def get_source(db: Session, source_id: int) -> Optional[Source]:
    """Get a source by ID."""
    return db.query(Source).filter(Source.id == source_id).first()

def get_source_by_url(db: Session, url: str) -> Optional[Source]:
    """Get a source by URL."""
    return db.query(Source).filter(Source.url == url).first()

def get_sources(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    source_type: Optional[str] = None
) -> List[Source]:
    """Get all sources with optional filtering by type."""
    query = db.query(Source)
    
    if source_type:
        query = query.filter(Source.source_type == source_type)
        
    return query.offset(skip).limit(limit).all()

def create_source(db: Session, source: SourceCreate) -> Source:
    """Create a new source."""
    # Convert Pydantic model to SQLAlchemy model
    db_source = Source(
        url=str(source.url),  # Convert URL to string
        title=source.title,
        description=source.description,
        source_type=source.source_type
    )
    
    # Add to session and commit
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    
    return db_source

def update_source(
    db: Session, 
    source_id: int, 
    source_update: SourceUpdate
) -> Optional[Source]:
    """Update an existing source."""
    # Get the source
    db_source = get_source(db, source_id)
    
    if not db_source:
        return None
    
    # Get the update data, excluding None values
    update_data = source_update.dict(exclude_unset=True)
    
    # If url is in the data, convert it to string
    if "url" in update_data and update_data["url"]:
        update_data["url"] = str(update_data["url"])
    
    # Update the source attributes
    for key, value in update_data.items():
        setattr(db_source, key, value)
    
    # Commit changes
    db.commit()
    db.refresh(db_source)
    
    return db_source

def delete_source(db: Session, source_id: int) -> bool:
    """Delete a source by ID."""
    db_source = get_source(db, source_id)
    
    if not db_source:
        return False
    
    db.delete(db_source)
    db.commit()
    
    return True
