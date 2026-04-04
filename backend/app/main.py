# app/main.py
# This is the entry point of our FastAPI backend
# Every request to the backend starts here

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the FastAPI app instance
# This is like creating our web server
app = FastAPI(
    title="DriveLegal API",
    description="AI-powered Indian Traffic Law Platform API",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI will be at /docs
    redoc_url="/redoc"     # ReDoc UI will be at /redoc
)

# CORS middleware — allows our React frontend to talk to this backend
# Without this, the browser would block frontend requests to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],   # Allow GET, POST, PUT, DELETE etc
    allow_headers=["*"],   # Allow all headers
)

# ─── ROUTES ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    """Root endpoint — confirms API is running"""
    return {
        "message": "Welcome to DriveLegal API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    Used by deployment platforms to verify the service is alive
    """
    return {
        "status": "healthy",
        "app": os.getenv("APP_NAME", "DriveLegal"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "debug": os.getenv("DEBUG", "False")
    }


@app.get("/api/v1/test")
def test_endpoint():
    """
    Test endpoint — confirms API routing works
    We will replace this with real routes in future steps
    """
    return {
        "message": "DriveLegal API is working!",
        "features": [
            "GPS-based law lookup",
            "Challan calculator", 
            "RTO directory",
            "AI plain-language explainer",
            "Know Your Rights guide",
            "Multilingual support",
            "Challan history tracker",
            "AI chat assistant",
            "PWA offline support",
            "Law change alerts",
            "WhatsApp sharing"
        ]
    }