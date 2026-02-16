# TitanForge: Build and Run Guide

This document provides standard commands for building, testing, and running TitanForge locally.

## Prerequisites

- **Node.js** 18+ (test: `node --version`)
- **npm** 8+ (test: `npm --version`)
- **Python** 3.11+ (test: `python --version`)
- **Docker** & **Docker Compose** (test: `docker --version`, `docker-compose --version`)
- **.env file** configured (see `.env.example` template)

## Environment Setup

### 1. Create .env file

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

**Required variables:**
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `STRIPE_API_KEY` (use test key: `sk_test_...`)
- `STRIPE_WEBHOOK_SECRET` (use test webhook secret)
- `OPENAI_API_KEY` or `GROQ_API_KEY` (for LLM)
- `SECRET_KEY` (JWT signing, generate with: `openssl rand -hex 32`)

### 2. Install Dependencies

#### Frontend
```bash
cd frontend
npm install
```

#### Backend
```bash
cd titanforge_backend
pip install -r requirements.txt
```

## Build Commands

### Frontend Build

**Development (watch mode):**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

**Production build:**
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

**Lint check:**
```bash
cd frontend
npm run lint
```

### Backend Build (Docker)

**Build Docker image:**
```bash
cd titanforge_backend
docker build -t titanforge-backend:latest .
```

**Verify image built:**
```bash
docker image ls | grep titanforge-backend
```

## Running Services

### Option A: Docker Compose (Recommended)

**Start all services:**
```bash
docker-compose up -d
```

This starts:
- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`
- FastAPI backend on `localhost:8000`

**Check service logs:**
```bash
docker-compose logs -f backend      # FastAPI logs
docker-compose logs -f db           # PostgreSQL logs
docker-compose logs -f redis        # Redis logs
```

**Stop all services:**
```bash
docker-compose down
```

**Stop and remove volumes (WARNING: deletes data):**
```bash
docker-compose down -v
```

### Option B: Local Development (Python directly)

**Prerequisites:** PostgreSQL and Redis running locally or via Docker

**Start only PostgreSQL and Redis:**
```bash
docker-compose up -d postgres redis
```

**Run FastAPI backend (from titanforge_backend/ dir):**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**In another terminal, run frontend (from frontend/ dir):**
```bash
npm run dev
```

## Test Commands

### Frontend Tests

**Lint (TypeScript/ESLint):**
```bash
cd frontend
npm run lint
```

*Note: No unit tests configured yet. See STEP 8 for test setup.*

### Backend Tests

**Run pytest:**
```bash
cd titanforge_backend
pytest
```

**Run with coverage:**
```bash
cd titanforge_backend
pytest --cov=app tests/
```

**Run specific test:**
```bash
cd titanforge_backend
pytest tests/test_main.py::test_health_check -v
```

## Verification Checklist

After setting up, verify everything works:

```bash
# 1. Check frontend builds
cd frontend
npm run build
echo "✓ Frontend builds successfully"

# 2. Check backend Docker image builds
cd ../titanforge_backend
docker build -t titanforge-backend:test .
echo "✓ Backend Docker image builds"

# 3. Start services
cd ..
docker-compose up -d
sleep 5  # Wait for services to start

# 4. Check PostgreSQL is running
docker-compose exec db psql -U titanforge_user -d titanforge_db -c "SELECT 1"
echo "✓ PostgreSQL is running"

# 5. Check Redis is running
docker-compose exec redis redis-cli ping
echo "✓ Redis is running"

# 6. Check backend API health (when ready)
curl http://localhost:8000/health
echo "✓ Backend API is running"

# 7. Stop services
docker-compose down
```

## Production Deployment

### Build for Production

**Backend:**
```bash
cd titanforge_backend
docker build -t titanforge-backend:prod .
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve dist/ folder with a web server (nginx, Apache, etc.)
```

### Environment Variables for Production

Update `.env` with production values:
- `ENV=PROD`
- `STRIPE_API_KEY` = live key (sk_live_...)
- `STRIPE_WEBHOOK_SECRET` = live webhook secret
- `SECRET_KEY` = secure random string
- `DATABASE_URL` = production PostgreSQL URL
- `REDIS_URL` = production Redis URL

### Docker Compose for Production

Use a production-grade compose file or Kubernetes manifests (coming soon).

## Troubleshooting

### Port Already in Use

**Issue:** `Error: listen EADDRINUSE: address already in use :::5173`

**Solution:**
```bash
# Find process using port
lsof -i :5173

# Or change port in vite.config.ts
```

### Database Connection Refused

**Issue:** Backend can't connect to PostgreSQL

**Solution:**
```bash
# Check if postgres is running
docker-compose ps

# Check database credentials in .env
# Make sure POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB match docker-compose.yml
```

### Import Errors in Backend

**Issue:** `ModuleNotFoundError: No module named '...'`

**Solution:**
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Check PYTHONPATH
export PYTHONPATH=/app
```

### Node version mismatch

**Issue:** `node: unsupported version`

**Solution:**
```bash
# Use nvm to switch versions or upgrade Node.js
nvm use 18
# or
npm install --global n
n 18
```

## Quick Start Commands

**One-liner to get everything running:**

```bash
# Terminal 1: Start services
docker-compose up

# Terminal 2: Start frontend
cd frontend && npm run dev

# Terminal 3: API should be ready at http://localhost:8000
#             Frontend at http://localhost:5173
```

## Next Steps

See `STEP 2` in the development plan for verifying endpoints and adding tests.
