"""
Vercel serverless function entry point for FastAPI backend
"""
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.main import app
from mangum import Mangum

# Wrap FastAPI app with Mangum for serverless deployment
handler = Mangum(app, lifespan="off")
