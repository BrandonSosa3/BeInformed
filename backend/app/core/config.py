import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This class manages all configuration settings for our application.
    BaseSettings from pydantic automatically reads from environment variables.
    """
    # Project information
    PROJECT_NAME: str = "BeInformed"
    API_V1_STR: str = "/api/v1"
    
    # Database connection settings
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "beinformednew_db")
    
    # Construct the database URL from individual components
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    
    class Config:
        # Tell pydantic to load variables from .env file
        env_file = ".env"

# Create a settings instance to use throughout the application
settings = Settings()