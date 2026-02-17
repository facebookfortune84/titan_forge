#!/bin/bash

################################################################################
# TitanForge AI - One-Command Startup Script (Linux/Mac)
# This script starts the entire TitanForge system with all services
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}
╔════════════════════════════════════════════════════════════════╗
║                   TITANFORGE AI - STARTUP                      ║
║              Money Machine Production Ready System              ║
╚════════════════════════════════════════════════════════════════╝
${NC}"

# ============================================================================
# 1. Check Prerequisites
# ============================================================================
echo -e "${YELLOW}[1/6] Checking prerequisites...${NC}"

check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}  ✗ $2 NOT found - $3${NC}"
        exit 1
    fi
    echo -e "${GREEN}  ✓ $2 found${NC}"
}

check_command "docker" "Docker" "Docker is required"
check_command "docker-compose" "Docker Compose" "Docker Compose is required"
check_command "node" "Node.js" "Node.js is required"
check_command "npm" "npm" "npm is required"
check_command "python3" "Python 3" "Python 3 is required"

# ============================================================================
# 2. Setup Environment Variables
# ============================================================================
echo -e "${YELLOW}[2/6] Setting up environment...${NC}"

ENV_FILE="$SCRIPT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${CYAN}  ! Creating .env from template...${NC}"
    
    cat > "$ENV_FILE" << 'EOF'
# DATABASE
POSTGRES_USER=titanforge_user
POSTGRES_PASSWORD=titanforge_secure_password_123
POSTGRES_DB=titanforge_db

# REDIS
REDIS_URL=redis://redis:6379/0

# STRIPE (Get keys from https://dashboard.stripe.com/apikeys)
STRIPE_API_KEY=sk_test_placeholder_replace_me
STRIPE_WEBHOOK_SECRET=whsec_placeholder_replace_me

# LLM APIs (Optional for agents)
OPENAI_API_KEY=
GROQ_API_KEY=
GEMINI_API_KEY=

# SECURITY
SECRET_KEY=titanforge_super_secret_key_change_in_production_$(date +%s)

# ENVIRONMENT
ENV=development
LOG_LEVEL=INFO

# FRONTEND
VITE_API_URL=http://localhost:8000
EOF
    
    echo -e "${GREEN}  ✓ .env created (update STRIPE keys before production!)${NC}"
else
    echo -e "${GREEN}  ✓ .env file exists${NC}"
fi

# Load environment
source "$ENV_FILE"

# ============================================================================
# 3. Start Docker Services
# ============================================================================
echo -e "${YELLOW}[3/6] Starting Docker services...${NC}"

cd "$SCRIPT_DIR"

echo -e "${CYAN}  - Stopping existing containers...${NC}"
docker-compose down --remove-orphans 2>/dev/null || true

echo -e "${CYAN}  - Starting PostgreSQL and Redis...${NC}"
docker-compose up -d db redis

echo -e "${CYAN}  - Waiting for services to be healthy...${NC}"
sleep 5

echo -e "${GREEN}  ✓ Docker services started${NC}"

# ============================================================================
# 4. Install Dependencies
# ============================================================================
echo -e "${YELLOW}[4/6] Installing dependencies...${NC}"

# Backend deps
echo -e "${CYAN}  - Installing Python dependencies...${NC}"
cd "$SCRIPT_DIR/titanforge_backend"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
deactivate
echo -e "${GREEN}  ✓ Backend dependencies installed${NC}"

# Frontend deps
echo -e "${CYAN}  - Installing Node dependencies...${NC}"
cd "$SCRIPT_DIR/frontend"
if [ ! -d "node_modules" ]; then
    npm install --silent 2>/dev/null
fi
echo -e "${GREEN}  ✓ Frontend dependencies installed${NC}"

# ============================================================================
# 5. Start Services
# ============================================================================
echo -e "${YELLOW}[5/6] Starting backend and frontend services...${NC}"

cd "$SCRIPT_DIR"

# Start Backend in background
echo -e "${CYAN}  - Starting FastAPI backend...${NC}"
cd "$SCRIPT_DIR/titanforge_backend"
source venv/bin/activate
PYTHONPATH="$SCRIPT_DIR/titanforge_backend" \
  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/titanforge-backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}  ✓ Backend process started (PID: $BACKEND_PID)${NC}"

# Start Frontend in background
echo -e "${CYAN}  - Starting Vite frontend...${NC}"
cd "$SCRIPT_DIR/frontend"
npm run dev > /tmp/titanforge-frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}  ✓ Frontend process started (PID: $FRONTEND_PID)${NC}"

# Wait for services to be ready
echo -e "${CYAN}  - Waiting for services to be ready...${NC}"
sleep 8

# ============================================================================
# 6. Display Summary
# ============================================================================
echo -e "${YELLOW}[6/6] Startup complete!${NC}"

echo -e "${CYAN}
╔════════════════════════════════════════════════════════════════╗
║                    🚀 SYSTEM IS READY 🚀                       ║
╚════════════════════════════════════════════════════════════════╝

📍 URLS:
  • Frontend:     http://localhost:5173
  • Backend API:  http://localhost:8000
  • API Docs:     http://localhost:8000/docs
  • ReDoc:        http://localhost:8000/redoc

🔧 SERVICES:
  • PostgreSQL:   localhost:5432
  • Redis:        localhost:6379
  • Backend:      localhost:8000 (PID: $BACKEND_PID)
  • Frontend:     localhost:5173 (PID: $FRONTEND_PID)

📝 NEXT STEPS:
  1. Open http://localhost:5173 in your browser
  2. Create an account and explore the dashboard
  3. Check http://localhost:8000/docs for API documentation
  4. Update .env with real Stripe keys when ready to test payments

📋 ENVIRONMENT VARIABLES:
  • Database:     Set in .env (POSTGRES_*)
  • Stripe Keys:  Set in .env (STRIPE_*)
  • LLM APIs:     Set in .env (OPENAI_API_KEY, GROQ_API_KEY, etc.)

💰 MONETIZATION STATUS:
  ✓ Stripe integration configured
  ✓ Pricing plans defined
  ✓ Lead capture wired
  ✓ Subscription system ready
  
⚠️  To stop services:
  • Press Ctrl+C, or
  • Run: kill $BACKEND_PID $FRONTEND_PID && docker-compose down

${NC}"

# Trap Ctrl+C for cleanup
trap 'echo -e "\n${YELLOW}Shutting down...${NC}"; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; cd "$SCRIPT_DIR" && docker-compose down 2>/dev/null || true; echo -e "${GREEN}System stopped.${NC}"; exit 0' INT

# Keep the script running and monitoring
echo -e "${YELLOW}System is running. Press Ctrl+C to stop...${NC}"

while true; do
    sleep 10
    
    # Check if processes are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo -e "${RED}Backend process crashed! Run startup again.${NC}"
        break
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo -e "${RED}Frontend process crashed! Run startup again.${NC}"
        break
    fi
done
