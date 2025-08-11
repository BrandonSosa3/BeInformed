# Import all models to make them available from the models package
from app.models.source import Source
from app.models.article import Article
from app.models.topic import Topic

# This ensures all models are imported when alembic runs
__all__ = ["Source", "Article", "Topic"]