from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",    # Local Vite frontend
        "http://localhost:3000",    # Local React default
        "https://be-informed-puce.vercel.app",  # Your Vercel URL
        "https://*.vercel.app",     # Any Vercel deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {"message": "Welcome to BeInformed API"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
