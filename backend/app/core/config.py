from typing import List

# Simple settings without using BaseSettings
class Settings:
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "BeInformed"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["*"]  # Allow all origins in development

# Create settings instance
settings = Settings()