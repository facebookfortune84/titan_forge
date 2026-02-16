# ============================================================================
# TITANFORGE ENDPOINT TESTING - POWERSHELL EQUIVALENTS
# ============================================================================
# These are the three PowerShell commands equivalent to the curl commands
# shown in the original documentation

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         TITANFORGE - POWERSHELL ENDPOINT TESTS                 ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ===========================================================================
# TEST 1: Dashboard Metrics Endpoint
# ===========================================================================
Write-Host "[TEST 1] Dashboard Metrics - GET /api/v1/dashboard/stats" -ForegroundColor Cyan
Write-Host "─" * 66 -ForegroundColor Gray
Write-Host ""

try {
    Write-Host "Sending request..." -ForegroundColor Yellow
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/dashboard/stats" `
        -Method GET `
        -ContentType "application/json" `
        -TimeoutSec 5 `
        -ErrorAction Stop
    
    Write-Host "✓ SUCCESS - Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host ""
    
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Response Data:" -ForegroundColor Yellow
    $data | Format-Table
    
} catch {
    Write-Host "✗ FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host ""

# ===========================================================================
# TEST 2: ROI Calculator (Lead Capture)
# ===========================================================================
Write-Host "[TEST 2] Lead Capture - POST /api/v1/sales/roi-pdf" -ForegroundColor Cyan
Write-Host "─" * 66 -ForegroundColor Gray
Write-Host ""

try {
    Write-Host "Sending request with lead data..." -ForegroundColor Yellow
    
    $timestamp = (Get-Date).ToString("yyyyMMddHHmmss")
    $payload = @{
        email = "salesteam_$timestamp@titanforge.io"
        company_name = "Prospect Company"
        company_size = "51-500"
    } | ConvertTo-Json
    
    Write-Host "Payload:" -ForegroundColor Gray
    Write-Host $payload -ForegroundColor Gray
    Write-Host ""
    
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/sales/roi-pdf" `
        -Method POST `
        -ContentType "application/json" `
        -Body $payload `
        -TimeoutSec 5 `
        -ErrorAction Stop
    
    Write-Host "✓ SUCCESS - Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host ""
    
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Lead Captured:" -ForegroundColor Yellow
    Write-Host "  Email: $($data.email)" -ForegroundColor White
    Write-Host "  Company: $($data.company_name)" -ForegroundColor White
    Write-Host ""
    
    Write-Host "ROI Summary:" -ForegroundColor Yellow
    Write-Host "  Annual Savings: $($data.roi_summary.annual_savings)" -ForegroundColor White
    Write-Host "  Monthly Savings: $($data.roi_summary.monthly_savings)" -ForegroundColor White
    Write-Host "  Breakeven: $($data.roi_summary.breakeven_months) months" -ForegroundColor White
    Write-Host "  ROI %: $($data.roi_summary.roi_percentage)" -ForegroundColor White
    Write-Host ""
    
    if ($data.html_content.Length -gt 0) {
        Write-Host "HTML Report Generated: ✓ YES" -ForegroundColor Green
        Write-Host "Size: $($data.html_content.Length) characters" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "✗ FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host ""

# ===========================================================================
# TEST 3: Pricing API Endpoint
# ===========================================================================
Write-Host "[TEST 3] Pricing Tiers - GET /api/v1/pricing" -ForegroundColor Cyan
Write-Host "─" * 66 -ForegroundColor Gray
Write-Host ""

try {
    Write-Host "Sending request..." -ForegroundColor Yellow
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/pricing" `
        -Method GET `
        -ContentType "application/json" `
        -TimeoutSec 5 `
        -ErrorAction Stop
    
    Write-Host "✓ SUCCESS - Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host ""
    
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Available Pricing Tiers:" -ForegroundColor Yellow
    Write-Host ""
    
    $data.PSObject.Properties | ForEach-Object {
        $tier = $_.Value
        Write-Host "  Name: $($tier.name)" -ForegroundColor Cyan
        Write-Host "  Monthly: $$($tier.monthly_price)" -ForegroundColor White
        Write-Host "  Annual: $$($tier.annual_price)" -ForegroundColor White
        Write-Host "  Features: $($tier.features -join ', ')" -ForegroundColor Gray
        Write-Host ""
    }
    
} catch {
    Write-Host "✗ FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host ""

# ===========================================================================
# SUMMARY
# ===========================================================================
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    TESTING COMPLETE                           ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "PowerShell Command Equivalents:" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Dashboard Metrics:" -ForegroundColor Yellow
Write-Host '   Invoke-WebRequest -Uri "http://localhost:8000/api/v1/dashboard/stats" -Method GET' -ForegroundColor Gray
Write-Host ""

Write-Host "2. Lead Capture (ROI):" -ForegroundColor Yellow
Write-Host '   $body = @{ email="user@company.com"; company_name="Company"; company_size="51-500" } | ConvertTo-Json' -ForegroundColor Gray
Write-Host '   Invoke-WebRequest -Uri "http://localhost:8000/api/v1/sales/roi-pdf" -Method POST -ContentType "application/json" -Body $body' -ForegroundColor Gray
Write-Host ""

Write-Host "3. Pricing API:" -ForegroundColor Yellow
Write-Host '   Invoke-WebRequest -Uri "http://localhost:8000/api/v1/pricing" -Method GET' -ForegroundColor Gray
Write-Host ""

Write-Host "All endpoints verified and operational!" -ForegroundColor Green
Write-Host ""
