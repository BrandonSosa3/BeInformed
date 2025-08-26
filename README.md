BeInformed – Media Bias & Sentiment Analysis Platform

A full-stack web application that analyzes news articles from multiple sources to highlight differences in sentiment, political bias, and factual reporting. BeInformed helps users understand media coverage from diverse perspectives and identify potential biases in reporting.

Project Overview

BeInformed provides AI-powered analysis of news articles through a clean, modern web interface. Users can search for topics, explore media sentiment, filter by political perspective, and view detailed analysis of individual articles.

Important Note for Users: When using the Vercel live demo, please allow up to 1-2 minutes on the first load. The backend is hosted on Render's free tier and spins down when idle. Because the backend includes heavy machine learning dependencies, it takes extra time to restart. Once running, subsequent interactions are fast and responsive. PLEASE also keep your searches to a minimum or just 1-2 as we are using free version of NewsApi which only alots a small number of requests to the api for article retrieval per month and per day.


Live Links

Live Application: https://be-informed-puce.vercel.app
API Backend: https://beinformed-backend.onrender.com
API Documentation: https://beinformed-backend.onrender.com/docs

Quick Start Guide

Visit the live demo at https://be-informed-puce.vercel.app
Search for a topic (e.g., "climate change", "artificial intelligence")
Click the blue view topic analysis button
Then click the purple analyze button to get an ai analysis
Click filter articles by sentiment, political perspective, or source
Click view details to see the one sentence ai summary and then be taken to linked full artice if desired

Key Features

Topic Search & Discovery – Find news coverage on any topic from diverse sources
Article Analysis – AI-powered sentiment, political bias, and factual reporting insights
Filtering System – Filter articles by sentiment, political perspective, and source
Responsive Design – Modern UI that works on desktop and mobile
Interactive Visualizations – Distribution of political perspectives across sources

Technology Stack
Frontend

React with TypeScript
TailwindCSS for styling
React Router for navigation
Recharts for data visualization
Deployed on Vercel

Backend

FastAPI (Python)
SQLAlchemy ORM
Natural Language Processing (NLP) for article analysis
PostgreSQL database (Supabase)
Deployed on Render

Database

PostgreSQL hosted on Supabase
Connection pooling for production reliability
Alembic for database migrations

Technical Highlights

Responsive React Components – Custom-built with TypeScript for type safety
Advanced State Management – Clean data flow and state organization
AI Integration – NLP algorithms for sentiment and bias detection
RESTful API Design – Structured endpoints with clear documentation
Performance Optimization – Efficient rendering and data fetching patterns

Local Development Setup
Prerequisites

Python 3.10+
Node.js 16+
PostgreSQL (or use remote Supabase database)

Clone the Repository
bashgit clone https://github.com/BrandonSosa3/beinformed.git
cd beinformed
Backend Setup
bashcd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Frontend Setup
bashcd frontend
npm install
npm run dev
Access Locally

Frontend: http://localhost:5173
Backend API: http://localhost:8000
API Documentation: http://localhost:8000/docs

Environment Variables
Backend (.env)
envPOSTGRES_SERVER=your-database-host
POSTGRES_USER=your-username
POSTGRES_PASSWORD=your-password
POSTGRES_DB=your-database-name
POSTGRES_PORT=5432
NEWS_API_KEY=your-news-api-key
Frontend
envVITE_API_URL=http://localhost:8000/api/v1  # Local development
Database Management
View Database (Supabase)

Go to your Supabase project dashboard
Click "Table Editor" to view and manage data
Use "SQL Editor" for custom queries

Run Migrations
bashcd backend
alembic upgrade head  # Apply all migrations
alembic revision --autogenerate -m "Description"  # Create new migration
Testing the API
Backend Health Check

Visit: http://localhost:8000/health (local) or https://beinformed-backend.onrender.com/health (production)
Should return: {"status": "healthy"}

Test Endpoints
Visit the interactive API documentation:

Local: http://localhost:8000/docs
Production: https://beinformed-backend.onrender.com/docs

Key endpoints to test:

GET /api/v1/sources - List all news sources
POST /api/v1/topics/search - Search for topics
GET /api/v1/topics/{id} - Get topic details
POST /api/v1/analysis/topics/{id}/analyze - Analyze topic sentiment

Deployment Architecture

Frontend: Vercel (Static hosting with edge functions)
Backend: Render (Container-based Python hosting)
Database: Supabase (Managed PostgreSQL with connection pooling)
CI/CD: Automatic deployment on git push

Performance Notes

Backend spins down after inactivity (free tier limitation)
Cold start: 1-2 minutes (due to ML dependencies)
Warm performance: sub-second response times
Production deployment would use always-on hosting for instant availability

Technical Highlights for Recruiters

Frontend: React with TypeScript, responsive design, interactive data visualizations
Backend: FastAPI with async operations, Pydantic validation, comprehensive error handling
AI/ML: News sentiment and bias detection, article summarization using NLTK
DevOps: Container deployment, environment-based configuration, database migrations
Best Practices: Modular architecture, type safety, comprehensive logging, user-friendly error handling


Debug Commands
bash# Check backend logs
curl https://beinformed-backend.onrender.com/health

# Test database connection
alembic current  # Shows current migration version

# Check frontend build
npm run build


Contact
Developer: Brandon Sosa

LinkedIn: https://www.linkedin.com/in/brandonsosa123/
GitHub: https://github.com/BrandonSosa3
Email: brandonsosa10101@gmail.com
Phone: 1(818)-309-6961