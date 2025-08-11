from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from app.db.base import get_db
from app.services.topic import topic_service
from app.models.topic import TopicArticle
from app.schemas.topic import Topic, TopicSearchRequest, TopicSearchResponse
from app.schemas.article import Article, ArticleList

router = APIRouter()

@router.get("/", response_model=List[Topic])
def read_topics(
    skip: int = 0,
    limit: int = 100,
    sort_by: str = Query("search_count", description="Field to sort by (search_count, name, created_at, last_searched_at)"),
    db: Session = Depends(get_db)
):
    """
    Get all topics with pagination and sorting.
    """
    topics = topic_service.get_topics(
        db=db, 
        skip=skip, 
        limit=limit, 
        sort_by=sort_by
    )
    return topics

@router.get("/{topic_id}", response_model=Topic)
def read_topic(
    topic_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific topic by ID.
    """
    topic = topic_service.get_topic(db, topic_id=topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.post("/search", response_model=TopicSearchResponse)
def search_topic(
    request: TopicSearchRequest,
    db: Session = Depends(get_db)
):
    """
    Search for a topic and collect articles about it.
    """
    result = topic_service.search_or_create_topic(
        db=db,
        topic_name=request.topic,
        collect_articles=True,
        max_articles=request.max_articles
    )
    
    # Format the response according to the schema
    response = {
        "topic": result["topic"],
        "is_new": result["is_new"],
        "articles_found": 0,
        "articles_stored": 0,
        "sources_found": 0,
        "sources_stored": 0,
        "errors": []
    }
    
    # Add collection results if available
    if result["collection_result"]:
        collection = result["collection_result"]
        response["articles_found"] = collection["articles_found"]
        response["articles_stored"] = collection["articles_stored"]
        response["sources_found"] = collection["sources_found"]
        response["sources_stored"] = collection["sources_stored"]
        response["errors"] = collection["errors"]
    
    return response

@router.get("/{topic_id}/articles", response_model=ArticleList)
def read_topic_articles(
    topic_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("published_at", description="Field to sort by (published_at, title, source_name)"),
    db: Session = Depends(get_db)
):
    """
    Get articles for a specific topic with pagination.
    """
    # Make sure the topic exists
    topic = topic_service.get_topic(db, topic_id=topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Calculate offset
    skip = (page - 1) * size
    
    # Get articles
    articles = topic_service.get_topic_articles(
        db=db,
        topic_id=topic_id,
        skip=skip,
        limit=size,
        sort_by=sort_by
    )
    
    # Count total articles for this topic
    total = db.query(TopicArticle).filter(TopicArticle.topic_id == topic_id).count()
    
    # Calculate total pages
    pages = math.ceil(total / size) if total > 0 else 1
    
    # Return response
    return {
        "items": articles,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }