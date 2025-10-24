# MyLitUK Backend

FastAPI backend for MyLitUK - Personalized UK Literature Platform

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Run Development Server

```bash
# From backend directory
python -m uvicorn app.main:app --reload --port 8000

# Or
python app/main.py
```

### 4. View API Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Authentication
│   │   ├── authors.py    # Authors endpoints
│   │   ├── books.py      # Books endpoints
│   │   ├── events.py     # Events endpoints
│   │   └── awards.py     # Awards endpoints
│   ├── core/             # Core functionality
│   │   └── config.py     # Settings
│   ├── db/               # Database
│   │   └── base.py       # DB setup
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── main.py           # FastAPI app
├── requirements.txt
├── .env.example
└── README.md
```

## 🗄️ Database

### PostgreSQL (Local Development)

```bash
# Using Docker
docker run --name postgres-mylituk \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=mylituk \
  -p 5432:5432 \
  -d postgres:15
```

### Supabase (Production - Free!)

1. Sign up at https://supabase.com
2. Create new project
3. Copy connection string to .env

## 🔧 Available Commands

### Run Server
```bash
uvicorn app.main:app --reload
```

### Run Tests
```bash
pytest
```

### Database Migrations (Coming soon)
```bash
alembic upgrade head
```

## 🌐 API Endpoints

### Core

- `GET /` - API info
- `GET /health` - Health check

### Authentication (Coming soon)

- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Authors (Coming soon)

- `GET /api/authors` - List authors
- `GET /api/authors/{id}` - Get author details
- `POST /api/authors/{id}/follow` - Follow author

### Dashboard (Coming soon)

- `GET /api/dashboard` - Personalized feed

## 📚 Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy 2.0** - ORM with async support
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **JWT** - Authentication

## 🎯 Development Status

- [x] Project setup
- [x] FastAPI app structure
- [x] Database configuration
- [ ] User models
- [ ] Authentication
- [ ] Author/Book models
- [ ] Event/Award models
- [ ] API endpoints
- [ ] Tests

## 📝 Notes

- Uses async/await for better performance
- Supports multilingual content (English/Korean)
- Designed for 100% free hosting (Render.com)
