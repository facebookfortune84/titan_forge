# ============================================================================
# TITANFORGE ENDPOINT TESTING - POWERSHELL EQUIVALENTS
# ============================================================================
# Run these commands to validate all critical endpoints
# Each command has detailed error handling and output

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TITANFORGE ENDPOINT VALIDATION SUITE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# TEST 1: FASTAPI DOCS ENDPOINT (Verifies backend is running)
# ============================================================================
Write-Host "[TEST 1] Checking FastAPI Docs Endpoint..." -ForegroundColor Yellow
Write-Host "Command: Invoke-RestMethod -Uri 'http://localhost:8000/docs' -ErrorAction Stop" -ForegroundColor Gray
Write-Host ""

try {
    $response1 = Invoke-RestMethod -Uri "http://localhost:8000/docs" -ErrorAction Stop
    Write-Host "✓ PASS: Backend is running on port 8000" -ForegroundColor Green
    Write-Host "  Response type: $($response1.GetType().Name)" -ForegroundColor Green
    Write-Host "  Swagger UI is accessible" -ForegroundColor Green
} catch {
    Write-Host "✗ FAIL: Backend not responding on :8000" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Action: Ensure backend is running with: python -m uvicorn app.main:app --reload" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# TEST 2: METRICS/DASHBOARD STATS ENDPOINT (JSON API)
# ============================================================================
Write-Host "[TEST 2] Checking Dashboard Stats API Endpoint..." -ForegroundColor Yellow
Write-Host "Command: Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/dashboard/stats' -Headers @{'Accept'='application/json'}" -ForegroundColor Gray
Write-Host ""

try {
    $response2 = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/dashboard/stats" `
        -Method Get `
        -Headers @{"Accept" = "application/json"} `
        -ErrorAction Stop
    
    Write-Host "✓ PASS: Dashboard stats endpoint is working" -ForegroundColor Green
    Write-Host "  Response: $(ConvertTo-Json $response2 -Compress)" -ForegroundColor Green
    Write-Host "  Data received successfully" -ForegroundColor Green
    
} catch {
    Write-Host "✗ FAIL: Dashboard stats endpoint error" -ForegroundColor Red
    Write-Host "  Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Action: Check if endpoint returns JSON (not HTML)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# TEST 3: REGISTRATION ENDPOINT (With CORS Headers)
# ============================================================================
Write-Host "[TEST 3] Checking Registration Endpoint (with CORS)..." -ForegroundColor Yellow
Write-Host "Command: Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/auth/register' -Method Post -Body @{...} -ContentType 'application/json'" -ForegroundColor Gray
Write-Host ""

try {
    $registerPayload = @{
        email    = "test@example.com"
        password = "SecurePassword123!"
        full_name = "Test User"
    } | ConvertTo-Json
    
    $response3 = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" `
        -Method Post `
        -Headers @{
            "Content-Type" = "application/json"
            "Origin" = "http://localhost:5173"
        } `
        -Body $registerPayload `
        -ErrorAction Stop
    
    Write-Host "✓ PASS: Registration endpoint is working" -ForegroundColor Green
    Write-Host "  User created successfully" -ForegroundColor Green
    Write-Host "  Response: $(ConvertTo-Json $response3 -Compress)" -ForegroundColor Green
    
} catch {
    $statusCode = $_.Exception.Response.StatusCode.Value__
    
    if ($statusCode -eq 409) {
        Write-Host "! INFO: User already exists (409)" -ForegroundColor Cyan
        Write-Host "  This is expected if already registered" -ForegroundColor Cyan
    } elseif ($statusCode -eq 422) {
        Write-Host "✗ FAIL: Validation error (422)" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Response.StatusDescription)" -ForegroundColor Red
    } elseif ($statusCode -eq 500) {
        Write-Host "✗ FAIL: Server error (500)" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "  Action: Check backend logs for database/connection issues" -ForegroundColor Yellow
    } elseif ($null -eq $statusCode) {
        Write-Host "✗ FAIL: Connection error" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "  Action: Verify backend is running on localhost:8000" -ForegroundColor Yellow
    } else {
        Write-Host "✗ FAIL: HTTP $statusCode error" -ForegroundColor Red
        Write-Host "  Error: $($_.Exception.Response.StatusDescription)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[SUITE COMPLETE]" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
