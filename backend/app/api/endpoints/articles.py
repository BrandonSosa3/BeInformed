from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.models.article import Article as ArticleModel
from app.schemas.article import Article, ArticleCreate, ArticleUpdate

router = APIRouter()

@router.get("/", response_model=List[Article])
def read_articles(
    skip: int = 0,
    limit: int = 100,
    source_id: Optional[int] = None,
    source_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all articles with optional filtering.
    """
    query = db.query(ArticleModel)
    
    # Apply filters
    if source_id is not None:
        query = query.filter(ArticleModel.source_id == source_id)
    if source_name is not None:
        query = query.filter(ArticleModel.source_name == source_name)
    
    # Apply pagination
    articles = query.order_by(ArticleModel.published_at.desc()).offset(skip).limit(limit).all()
    
    return articles

@router.get("/{article_id}", response_model=Article)
def read_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific article by ID.
    """
    article = db.query(ArticleModel).filter(ArticleModel.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article