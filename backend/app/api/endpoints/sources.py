from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.services import source as source_service
from app.schemas.source import Source, SourceCreate, SourceUpdate

router = APIRouter()

@router.get("/", response_model=List[Source])
def read_sources(
    skip: int = 0,
    limit: int = 100,
    source_type: Optional[str] = Query(None, description="Filter by source type"),
    db: Session = Depends(get_db)
):
    """
    Get all sources with optional filtering.
    """
    sources = source_service.get_sources(
        db, skip=skip, limit=limit, source_type=source_type
    )
    return sources

@router.post("/", response_model=Source, status_code=201)
def create_source(
    source: SourceCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new source.
    """
    db_source = source_service.get_source_by_url(db, url=str(source.url))
    if db_source:
        raise HTTPException(
            status_code=400,
            detail="Source with this URL already exists"
        )
    return source_service.create_source(db=db, source=source)

@router.get("/{source_id}", response_model=Source)
def read_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific source by ID.
    """
    db_source = source_service.get_source(db, source_id=source_id)
    if db_source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return db_source

@router.put("/{source_id}", response_model=Source)
def update_source(
    source_id: int,
    source_update: SourceUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a source.
    """
    db_source = source_service.update_source(
        db, source_id=source_id, source_update=source_update
    )
    if db_source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return db_source

@router.delete("/{source_id}", status_code=204)
def delete_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a source.
    """
    success = source_service.delete_source(db, source_id=source_id)
    if not success:
        raise HTTPException(status_code=404, detail="Source not found")
    return None
