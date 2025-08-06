from fastapi import APIRouter

from app.api.endpoints import sources

api_router = APIRouter()
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
