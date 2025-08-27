from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from fastapi import Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000", 
        "https://be-informed-puce.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
    ],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {"message": "Welcome to BeInformed API"}

@app.get("/db-test")
async def test_db():
    try:
        # Add your database connection test here
        # This depends on how your database is configured
        return {"status": "database connected"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.options("/health") 
async def health_options():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )