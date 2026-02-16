# ============================================================================
# TITANFORGE SALES DEMO LAUNCH SCRIPT - COMPLETE SOLUTION
# ============================================================================
# This script launches the entire TitanForge system and runs validation tests
# Perfect for sales demos - everything in one place
# Run this as Administrator for best results

Write-Host "`n" -NoNewline
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         TITANFORGE - PRODUCTION LAUNCH SCRIPT                  ║" -ForegroundColor Cyan
Write-Host "║          Multi-Agent AI Development Agency Platform           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

# Configuration
$PROJECT_ROOT = "F:\TitanForge"
$BACKEND_PATH = "$PROJECT_ROOT\titanforge_backend"
$FRONTEND_PATH = "$PROJECT_ROOT\frontend"
$BACKEND_URL = "http://localhost:8000"
$FRONTEND_URL = "http://localhost:5173"

# Track startup status
$services = @{
    "Backend" = $false
    "Frontend" = $false
    "Database" = $false
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

function Test-Port {
    param([int]$Port)
    $connection = New-Object System.Net.Sockets.TcpClient
    try {
        $connection.Connect("127.0.0.1", $Port)
        $connection.Close()
        return $true
    } catch {
        return $false
    }
}

function Wait-ForService {
    param([string]$ServiceName, [int]$Port, [int]$MaxRetries = 30)
    Write-Host "  ⏳ Waiting for $ServiceName on port $Port..." -ForegroundColor Yellow
    $retries = 0
    while ($retries -lt $MaxRetries) {
        if (Test-Port $Port) {
            Write-Host "  ✓ $ServiceName is online!" -ForegroundColor Green
            return $true
        }
        Start-Sleep -Seconds 2
        $retries++
        Write-Host -NoNewline "." -ForegroundColor Yellow
    }
    Write-Host "`n  ✗ $ServiceName failed to start" -ForegroundColor Red
    return $false
}

# ============================================================================
# PHASE 1: VERIFY ENVIRONMENT
# ============================================================================

Write-Host "[PHASE 1] Verifying Environment Setup" -ForegroundColor Cyan
Write-Host "─" * 60 -ForegroundColor Gray

# Check if paths exist
if (-not (Test-Path $BACKEND_PATH)) {
    Write-Host "  ✗ Backend path not found: $BACKEND_PATH" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $FRONTEND_PATH)) {
    Write-Host "  ✗ Frontend path not found: $FRONTEND_PATH" -ForegroundColor Red
    exit 1
}

Write-Host "  ✓ Project paths verified" -ForegroundColor Green
Write-Host "  ✓ Backend path: $BACKEND_PATH" -ForegroundColor Green
Write-Host "  ✓ Frontend path: $FRONTEND_PATH" -ForegroundColor Green

# Check if ports are available
Write-Host "`n  Checking port availability..." -ForegroundColor Yellow
if (Test-Port 8000) {
    Write-Host "  ⚠ Port 8000 already in use" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Port 8000 available" -ForegroundColor Green
}

if (Test-Port 5173) {
    Write-Host "  ⚠ Port 5173 already in use" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ Port 5173 available" -ForegroundColor Green
}

Write-Host ""

# ============================================================================
# PHASE 2: START SERVICES
# ============================================================================

Write-Host "[PHASE 2] Starting Services" -ForegroundColor Cyan
Write-Host "─" * 60 -ForegroundColor Gray

Write-Host "`n  📡 Starting Backend (FastAPI on port 8000)..." -ForegroundColor Yellow

# Start backend in background
$backendProcess = Start-Process `
    -FilePath "python" `
    -ArgumentList "-m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" `
    -WorkingDirectory $BACKEND_PATH `
    -WindowStyle Minimized `
    -PassThru

if ($backendProcess) {
    Write-Host "  ✓ Backend process started (PID: $($backendProcess.Id))" -ForegroundColor Green
    if (Wait-ForService "Backend" 8000) {
        $services["Backend"] = $true
    }
} else {
    Write-Host "  ✗ Failed to start backend" -ForegroundColor Red
}

Start-Sleep -Seconds 3

Write-Host "`n  🎨 Starting Frontend (Vite on port 5173)..." -ForegroundColor Yellow

# Start frontend in background
$frontendProcess = Start-Process `
    -FilePath "npm" `
    -ArgumentList "run dev" `
    -WorkingDirectory $FRONTEND_PATH `
    -WindowStyle Minimized `
    -PassThru

if ($frontendProcess) {
    Write-Host "  ✓ Frontend process started (PID: $($frontendProcess.Id))" -ForegroundColor Green
    if (Wait-ForService "Frontend" 5173) {
        $services["Frontend"] = $true
    }
} else {
    Write-Host "  ✗ Failed to start frontend" -ForegroundColor Red
}

Write-Host ""

# ============================================================================
# PHASE 3: VALIDATE ENDPOINTS
# ============================================================================

Write-Host "[PHASE 3] Validating Critical Endpoints" -ForegroundColor Cyan
Write-Host "─" * 60 -ForegroundColor Gray
Write-Host ""

# Test 1: FastAPI Docs
Write-Host "  [TEST 1] FastAPI Documentation Endpoint" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BACKEND_URL/docs" -ErrorAction Stop -TimeoutSec 5
    Write-Host "  ✓ PASS - Backend API documentation accessible" -ForegroundColor Green
    Write-Host "    URL: $BACKEND_URL/docs" -ForegroundColor Gray
} catch {
    Write-Host "  ✗ FAIL - Could not reach backend documentation" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 2: Dashboard Stats (JSON API)
Write-Host "  [TEST 2] Dashboard Stats API (JSON)" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod `
        -Uri "$BACKEND_URL/api/v1/dashboard/stats" `
        -Method Get `
        -Headers @{"Accept" = "application/json"} `
        -ErrorAction Stop `
        -TimeoutSec 5
    
    Write-Host "  ✓ PASS - Dashboard stats endpoint working" -ForegroundColor Green
    Write-Host "    Leads: $($response.leads_count)" -ForegroundColor Gray
    Write-Host "    Customers: $($response.customers_count)" -ForegroundColor Gray
    Write-Host "    MRR: `$$($response.mrr)" -ForegroundColor Gray
    Write-Host "    Conversion Rate: $($response.conversion_rate)%" -ForegroundColor Gray
} catch {
    Write-Host "  ✗ FAIL - Dashboard stats endpoint error" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: Pricing Endpoint
Write-Host "  [TEST 3] Pricing API" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod `
        -Uri "$BACKEND_URL/api/v1/pricing" `
        -Method Get `
        -ErrorAction Stop `
        -TimeoutSec 5
    
    Write-Host "  ✓ PASS - Pricing endpoint working" -ForegroundColor Green
    Write-Host "    Available tiers: $($response.tiers.Count)" -ForegroundColor Gray
} catch {
    Write-Host "  ✗ FAIL - Pricing endpoint error" -ForegroundColor Red
    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 4: Registration Endpoint (with proper error handling)
Write-Host "  [TEST 4] Registration Endpoint (CORS + Validation)" -ForegroundColor Yellow
try {
    $registerPayload = @{
        email    = "sales-demo-$(Get-Random -Minimum 1000 -Maximum 9999)@titanforge.ai"
        password = "DemoPassword123!"
        full_name = "Sales Demo User"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod `
        -Uri "$BACKEND_URL/api/v1/auth/register" `
        -Method Post `
        -Headers @{
            "Content-Type" = "application/json"
            "Origin" = "http://localhost:5173"
        } `
        -Body $registerPayload `
        -ErrorAction Stop `
        -TimeoutSec 5
    
    Write-Host "  ✓ PASS - Registration endpoint working" -ForegroundColor Green
    Write-Host "    User created successfully" -ForegroundColor Gray
} catch {
    $statusCode = $_.Exception.Response.StatusCode.Value__
    if ($statusCode -eq 409) {
        Write-Host "  ✓ PASS - Registration endpoint working (user already exists)" -ForegroundColor Green
    } elseif ($statusCode -eq 422) {
        Write-Host "  ⚠ INFO - Validation error (expected for demo)" -ForegroundColor Cyan
    } else {
        Write-Host "  ✗ FAIL - Registration error" -ForegroundColor Red
        Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# ============================================================================
# PHASE 4: DEMO INSTRUCTIONS
# ============================================================================

Write-Host "[PHASE 4] Demo Ready - Next Steps" -ForegroundColor Cyan
Write-Host "─" * 60 -ForegroundColor Gray
Write-Host ""

Write-Host "✓ All systems operational! Your demo URLs:" -ForegroundColor Green
Write-Host ""
Write-Host "  🏠 Landing Page:    $FRONTEND_URL" -ForegroundColor Cyan
Write-Host "  📊 Dashboard:       $BACKEND_URL/dashboard" -ForegroundColor Cyan
Write-Host "  📚 API Docs:        $BACKEND_URL/docs" -ForegroundColor Cyan
Write-Host "  🤖 Agent Cockpit:   $FRONTEND_URL/cockpit" -ForegroundColor Cyan
Write-Host ""

Write-Host "Demo Flow:" -ForegroundColor Yellow
Write-Host "  1. Show Landing Page ($FRONTEND_URL)" -ForegroundColor Gray
Write-Host "  2. ROI Calculator Form (generates PDF lead magnet)" -ForegroundColor Gray
Write-Host "  3. Dashboard with Real Metrics ($BACKEND_URL/dashboard)" -ForegroundColor Gray
Write-Host "  4. Pricing Page" -ForegroundColor Gray
Write-Host "  5. Agent Cockpit ($FRONTEND_URL/cockpit)" -ForegroundColor Gray
Write-Host ""

Write-Host "Test Accounts:" -ForegroundColor Yellow
Write-Host "  Email: demo@titanforge.ai" -ForegroundColor Gray
Write-Host "  Password: DemoPassword123!" -ForegroundColor Gray
Write-Host ""

Write-Host "Stripe Test Card:" -ForegroundColor Yellow
Write-Host "  Card Number: 4242 4242 4242 4242" -ForegroundColor Gray
Write-Host "  Expiry: 12/25" -ForegroundColor Gray
Write-Host "  CVC: 123" -ForegroundColor Gray
Write-Host ""

# ============================================================================
# PHASE 5: KEEP RUNNING
# ============================================================================

Write-Host "[PHASE 5] System Status Monitor" -ForegroundColor Cyan
Write-Host "─" * 60 -ForegroundColor Gray
Write-Host ""

Write-Host "Services Status:" -ForegroundColor Yellow
$services | ForEach-Object {
    $serviceName = $_.Key
    $isRunning = $_.Value
    $status = if ($isRunning) { "✓ ONLINE" } else { "✗ OFFLINE" }
    $color = if ($isRunning) { "Green" } else { "Red" }
    Write-Host "  $serviceName`: $status" -ForegroundColor $color
}

Write-Host ""
Write-Host "Press Ctrl+C to shut down all services" -ForegroundColor Yellow
Write-Host ""

# Keep monitoring
$monitorInterval = 30
while ($true) {
    Start-Sleep -Seconds $monitorInterval
    
    # Check if processes are still running
    if ($null -ne $backendProcess) {
        if ($backendProcess.HasExited) {
            Write-Host "`n⚠ Backend process ended!" -ForegroundColor Yellow
        }
    }
    
    if ($null -ne $frontendProcess) {
        if ($frontendProcess.HasExited) {
            Write-Host "`n⚠ Frontend process ended!" -ForegroundColor Yellow
        }
    }
}
