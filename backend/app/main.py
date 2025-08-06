from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router

app = FastAPI(
    title="BeInformed API",
    description="API for BeInformed - Intelligent Information Analysis Platform",
    version="0.1.0"
)

# Configure CORS to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {"message": "Welcome to BeInformed API"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
