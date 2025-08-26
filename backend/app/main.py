from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # React default port
        "http://localhost:5173",    # Vite default port (your current frontend)
        "http://localhost:3001",    # Alternative React port
        "https://*.vercel.app",     # For production deployment
    ],
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
