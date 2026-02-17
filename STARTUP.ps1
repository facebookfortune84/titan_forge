#############################################################################
# TitanForge AI - One-Command Startup Script
# This script starts the entire TitanForge system with all services
#############################################################################

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=========================================================="
Write-Host "         TITANFORGE AI - STARTUP                  "
Write-Host "      Money Machine Production Ready System       "
Write-Host "==========================================================" -ForegroundColor Cyan

# ============================================================================
# 1. Check Prerequisites
# ============================================================================
Write-Host "[1/6] Checking prerequisites..." -ForegroundColor Yellow

$checks = @(
    ("Docker", { docker --version }, "Docker is required"),
    ("Docker Compose", { docker-compose --version }, "Docker Compose is required"),
    ("Node.js", { node --version }, "Node.js is required"),
    ("npm", { npm --version }, "npm is required"),
    ("Python 3.9+", { python --version }, "Python 3.9+ is required")
)

foreach ($check in $checks) {
    try {
        & $check[1] *> $null
        Write-Host ("  [OK] " + $check[0] + " found") -ForegroundColor Green
    } catch {
        Write-Host ("  [FAIL] " + $check[0] + " NOT found - " + $check[2]) -ForegroundColor Red
        exit 1
    }
}

# ============================================================================
# 2. Setup Environment Variables
# ============================================================================
Write-Host "[2/6] Setting up environment..." -ForegroundColor Yellow

$envFile = Join-Path $ScriptDir ".env"
if (-not (Test-Path $envFile)) {
    Write-Host "  ! Creating .env from template..." -ForegroundColor Cyan
    
    $envContent = @"
# DATABASE
POSTGRES_USER=titanforge_user
POSTGRES_PASSWORD=titanforge_secure_password_123
POSTGRES_DB=titanforge_db

# REDIS
REDIS_URL=redis://redis:6379/0

# STRIPE
STRIPE_API_KEY=sk_test_placeholder_replace_me
STRIPE_WEBHOOK_SECRET=whsec_placeholder_replace_me

# LLM APIs
OPENAI_API_KEY=
GROQ_API_KEY=
GEMINI_API_KEY=

# SECURITY
SECRET_KEY=titanforge_super_secret_key_change_in_production_$((Get-Random -Minimum 100000 -Maximum 999999))

# ENVIRONMENT
ENV=development
LOG_LEVEL=INFO

# FRONTEND
VITE_API_URL=http://localhost:8000
"@
    
    $envContent | Set-Content $envFile
    Write-Host "  [OK] .env created (update STRIPE keys before production!)" -ForegroundColor Green
} else {
    Write-Host "  [OK] .env file exists" -ForegroundColor Green
}

# ============================================================================
# 3. Start Docker Services
# ============================================================================
Write-Host "[3/6] Starting Docker services..." -ForegroundColor Yellow

Push-Location $ScriptDir
try {
    Write-Host "  - Stopping existing containers..." -ForegroundColor Cyan
    docker-compose down --remove-orphans 2>&1 | Where-Object { $_ -notmatch "obsolete" } | Out-Null
    
    Write-Host "  - Starting PostgreSQL and Redis..." -ForegroundColor Cyan
    docker-compose up -d db redis 2>&1 | Where-Object { $_ -notmatch "obsolete" } | Out-Null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  [FAIL] Failed to start Docker services" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "  - Waiting for services to be healthy..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
    
    Write-Host "  [OK] Docker services started" -ForegroundColor Green
} finally {
    Pop-Location
}

# ============================================================================
# 4. Install Dependencies
# ============================================================================
Write-Host "[4/6] Installing dependencies..." -ForegroundColor Yellow

# Backend deps
Write-Host "  - Installing Python dependencies..." -ForegroundColor Cyan
Push-Location (Join-Path $ScriptDir "titanforge_backend")
try {
    if (-not (Test-Path "venv")) {
        python -m venv venv
    }
    & ".\venv\Scripts\Activate.ps1"
    pip install -q -r requirements.txt 2>&1 | Out-Null
    Write-Host "  [OK] Backend dependencies installed" -ForegroundColor Green
} finally {
    Pop-Location
}

# Frontend deps
Write-Host "  - Installing Node dependencies..." -ForegroundColor Cyan
Push-Location (Join-Path $ScriptDir "frontend")
try {
    if (-not (Test-Path "node_modules")) {
        npm install --silent 2>&1 | Out-Null
    }
    Write-Host "  [OK] Frontend dependencies installed" -ForegroundColor Green
} finally {
    Pop-Location
}

# ============================================================================
# 5. Start Services
# ============================================================================
Write-Host "[5/6] Starting backend and frontend services..." -ForegroundColor Yellow

# Start Backend in background
Write-Host "  - Starting FastAPI backend..." -ForegroundColor Cyan
$backendProcess = Start-Process powershell -ArgumentList @"
    cd '$ScriptDir\titanforge_backend'
    `$env:PYTHONPATH = '$ScriptDir\titanforge_backend'
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"@ -PassThru -NoNewWindow
Write-Host ("  [OK] Backend process started (PID: " + $backendProcess.Id + ")") -ForegroundColor Green

# Start Frontend in background
Write-Host "  - Starting Vite frontend..." -ForegroundColor Cyan
$frontendProcess = Start-Process powershell -ArgumentList @"
    cd '$ScriptDir\frontend'
    npm run dev
"@ -PassThru -NoNewWindow
Write-Host ("  [OK] Frontend process started (PID: " + $frontendProcess.Id + ")") -ForegroundColor Green

# Wait for services to be ready
Write-Host "  - Waiting for services to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 8

# ============================================================================
# 6. Display Summary
# ============================================================================
Write-Host "[6/6] Startup complete!" -ForegroundColor Yellow

Write-Host ""
Write-Host "=========================================================="
Write-Host "            SYSTEM IS READY                     "
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "URLS:"
Write-Host "  * Frontend:     http://localhost:5173"
Write-Host "  * Backend API:  http://localhost:8000"
Write-Host "  * API Docs:     http://localhost:8000/docs"
Write-Host "  * ReDoc:        http://localhost:8000/redoc"
Write-Host ""
Write-Host "SERVICES:"
Write-Host "  * PostgreSQL:   localhost:5432"
Write-Host "  * Redis:        localhost:6379"
Write-Host ("  * Backend:      localhost:8000 (PID: " + $backendProcess.Id + ")")
Write-Host ("  * Frontend:     localhost:5173 (PID: " + $frontendProcess.Id + ")")
Write-Host ""
Write-Host "NEXT STEPS:"
Write-Host "  1. Open http://localhost:5173 in your browser"
Write-Host "  2. Create an account and explore the dashboard"
Write-Host "  3. Check http://localhost:8000/docs for API documentation"
Write-Host "  4. Update .env with real Stripe keys when ready"
Write-Host ""
Write-Host "=========================================================="
Write-Host ""

# Keep the script running and monitoring
Write-Host "System is running. Press Ctrl+C to stop..." -ForegroundColor Yellow
Write-Host ""

try {
    while ($true) {
        Start-Sleep -Seconds 10
        
        # Check if processes are still running
        if (-not (Get-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue)) {
            Write-Host "Backend process crashed! Run startup again." -ForegroundColor Red
            break
        }
        if (-not (Get-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue)) {
            Write-Host "Frontend process crashed! Run startup again." -ForegroundColor Red
            break
        }
    }
}
catch {
    Write-Host "Shutdown initiated..." -ForegroundColor Yellow
}
finally {
    Write-Host "Cleaning up..." -ForegroundColor Yellow
    Stop-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue
    Stop-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue
    Push-Location $ScriptDir
    docker-compose down 2>&1 | Out-Null
    Pop-Location
    Write-Host "System stopped." -ForegroundColor Green
}
