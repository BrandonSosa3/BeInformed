from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.base import get_db
from app.services.analysis.article_analyzer import article_analysis_service
from app.models.article import Article
from app.models.topic import Topic

router = APIRouter()

@router.post("/topics/{topic_id}/analyze")
async def analyze_topic_articles(
    topic_id: int,
    background_tasks: BackgroundTasks,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Analyze articles for a specific topic.
    
    Args:
        topic_id: ID of the topic
        limit: Maximum number of articles to analyze
        
    Returns:
        Dict with status message
    """
    # Check if topic exists
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Add the analysis task to background tasks
    background_tasks.add_task(
        article_analysis_service.analyze_articles_by_topic,
        db=db,
        topic_id=topic_id,
        limit=limit
    )
    
    return {
        "status": "Analysis started",
        "topic_id": topic_id,
        "topic_name": topic.name,
        "message": f"Analyzing up to {limit} articles for topic '{topic.name}'"
    }

@router.post("/articles/{article_id}/analyze")
async def analyze_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """
    Analyze a specific article.
    
    Args:
        article_id: ID of the article
        
    Returns:
        Dict with analysis results
    """
    # Get the article
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Analyze the article
    result = article_analysis_service.analyze_article(article, db)
    
    return {
        "status": "Analysis completed",
        "article_id": article.id,
        "article_title": article.title,
        "sentiment": {
            "score": article.sentiment_score,
            "label": article.sentiment_label,
            "confidence": article.sentiment_confidence
        },
        "last_analyzed_at": article.last_analyzed_at
    }

@router.post("/recent/analyze")
async def analyze_recent_articles(
    background_tasks: BackgroundTasks,
    days: int = 7,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Analyze recent articles.
    
    Args:
        days: Number of days to look back
        limit: Maximum number of articles to analyze
        
    Returns:
        Dict with status message
    """
    # Add the analysis task to background tasks
    background_tasks.add_task(
        article_analysis_service.analyze_recent_articles,
        db=db,
        days=days,
        limit=limit
    )
    
    return {
        "status": "Analysis started",
        "message": f"Analyzing up to {limit} articles from the last {days} days"
    }