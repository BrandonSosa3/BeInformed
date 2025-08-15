from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.services.statistics import statistics_service
from app.models.topic import Topic

router = APIRouter()

@router.get("/topics/{topic_id}")
def get_topic_statistics(
    topic_id: int,
    days: int = Query(30, description="Number of days to include (0 for all time)"),
    db: Session = Depends(get_db)
):
    """
    Get aggregate statistics for a topic.
    
    Args:
        topic_id: ID of the topic
        days: Number of days to include (0 for all time)
        
    Returns:
        Dict with topic statistics
    """
    # Check if topic exists
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Get topic statistics
    stats = statistics_service.get_topic_statistics(db, topic_id, days)
    
    return stats

@router.get("/topics/{topic_id}/sources")
def get_topic_source_statistics(
    topic_id: int,
    db: Session = Depends(get_db)
):
    """
    Get statistics about sources for a topic.
    
    Args:
        topic_id: ID of the topic
        
    Returns:
        List of sources with statistics
    """
    # Check if topic exists
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Get source statistics
    stats = statistics_service.get_source_statistics(db, topic_id)
    
    return stats

@router.get("/topics/{topic_id}/sentiment-over-time")
def get_sentiment_over_time(
    topic_id: int,
    days: int = Query(30, description="Number of days to include"),
    interval: str = Query("day", description="Time interval for grouping ('day', 'week', 'month')"),
    db: Session = Depends(get_db)
):
    """
    Get sentiment trends over time for a topic.
    
    Args:
        topic_id: ID of the topic
        days: Number of days to include
        interval: Time interval for grouping ('day', 'week', 'month')
        
    Returns:
        Dict with dates and sentiment values
    """
    # Check if topic exists
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Validate interval
    valid_intervals = ["day", "week", "month"]
    if interval not in valid_intervals:
        raise HTTPException(status_code=400, detail=f"Invalid interval. Must be one of: {', '.join(valid_intervals)}")
    
    # Get sentiment over time data
    data = statistics_service.get_sentiment_over_time(db, topic_id, days, interval)
    
    return data