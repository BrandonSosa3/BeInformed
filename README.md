BeInformed – Media Bias & Sentiment Analysis Platform

A full-stack web application that analyzes news articles from multiple sources to highlight differences in sentiment, political bias, and factual reporting. BeInformed helps users understand media coverage from diverse perspectives and identify potential biases in reporting.

Project Overview

BeInformed provides AI-powered analysis of news articles through a clean, modern web interface. Users can search for topics, explore media sentiment, filter by political perspective, and view detailed analysis of individual articles.

Important Note for Users: When using the Vercel live demo, please allow up to 3-7 minutes on the first load. The backend is hosted on Render’s free tier and spins down when idle. Because the backend includes heavy machine learning dependencies, it takes extra time to restart. Once running, subsequent interactions are fast and responsive.

Live Links:

Live Application: https://beInformed.vercel.app

API Backend: BeInformed API

Quick Start Guide

Visit the live demo at beinformed.vercel.app

Search for a topic (e.g., "climate change", "artificial intelligence")

Explore analyzed articles with sentiment, bias, and factual reporting indicators

Filter articles by sentiment, political perspective, or source

View detailed analysis of individual articles

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

Backend

FastAPI (Python)

SQLAlchemy ORM

Natural Language Processing (NLP) for article analysis

PostgreSQL database

Technical Highlights

Responsive React Components – Custom-built with TypeScript for type safety

Advanced State Management – Clean data flow and state organization

AI Integration – NLP algorithms for sentiment and bias detection

RESTful API Design – Structured endpoints with clear documentation

Performance Optimization – Efficient rendering and data fetching patterns

Local Setup:

Clone the repository:

git clone https://github.com/BrandonSosa3/beinformed.git
cd beinformed

Backend Setup:

cd backend python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate pip install -r requirements.txt cp .env.example .env uvicorn app.main:app --reload --port 8000

Frontend setup:

cd frontend npm install npm run dev


Visit locally:
http://localhost:5173

Performance Notes

Backend spins down after inactivity (free tier limitation).

Cold start: 3-7 minutes (due to ML dependencies).

Warm performance: sub-second response times.

Production deployment would use always-on hosting for instant availability.

Technical Highlights for Recruiters

Frontend: React with TypeScript, responsive design, interactive map UI.

Backend: FastAPI with async operations, pydantic validation, error handling.

AI/ML: News sentiment and bias detection, article summarization.

DevOps: Docker containerization, deployment on Vercel and Render.

Best Practices: Modular architecture, type safety, comprehensive logging, user-friendly error handling.

Contact

Developer: Brandon Sosa

LinkedIn: https://www.linkedin.com/in/brandonsosa123/ 

GitHub: https://github.com/BrandonSosa3 

Email: brandonsosa10101@gmail.com

Phone number: 1(818)-309-6961