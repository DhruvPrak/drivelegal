# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.routers import laws, fines, rto

load_dotenv()

app = FastAPI(
    title="DriveLegal API",
    description="AI-powered Indian Traffic Law Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(laws.router)
app.include_router(fines.router)
app.include_router(rto.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to DriveLegal API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app": os.getenv("APP_NAME", "DriveLegal"),
        "version": os.getenv("APP_VERSION", "1.0.0")
    }