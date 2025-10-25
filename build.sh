#!/bin/bash

# Vercel build script - Initialize database with sample data

echo "Initializing database..."

# Create tables
python -c "
import sys
sys.path.insert(0, 'backend')
from app.core.database import Base, engine
Base.metadata.create_all(bind=engine)
print('Tables created successfully')
"

# Seed sample data
python backend/seed_data.py

echo "Database initialized with sample data"
