from fastapi import APIRouter

from app.api.endpoints import sources, topics, articles

api_router = APIRouter()
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
