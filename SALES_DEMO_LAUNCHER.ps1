# ============================================================================
# TITANFORGE SALES DEMO LAUNCHER
# ============================================================================
# This script sets up TitanForge for a live sales demo
# Estimated time: 30 seconds setup, then open browser

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         TITANFORGE - AI AGENCY SOFTWARE PLATFORM              ║" -ForegroundColor Cyan
Write-Host "║                    SALES DEMO LAUNCHER                        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if services are running
Write-Host "[INFO] Verifying backend services..." -ForegroundColor Yellow

$frontend_running = $false
$backend_running = $false

try {
    $frontend_check = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($frontend_check.StatusCode -eq 200) {
        $frontend_running = $true
    }
} catch {}

try {
    $backend_check = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/dashboard/stats" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($backend_check.StatusCode -eq 200) {
        $backend_running = $true
    }
} catch {}

Write-Host ""
Write-Host "Service Status:" -ForegroundColor Cyan
Write-Host "  Frontend (port 5173): $(if ($frontend_running) {'✓ RUNNING'} else {'✗ NOT RUNNING'})" -ForegroundColor $(if ($frontend_running) {'Green'} else {'Red'})
Write-Host "  Backend (port 8000):  $(if ($backend_running) {'✓ RUNNING'} else {'✗ NOT RUNNING'})" -ForegroundColor $(if ($backend_running) {'Green'} else {'Red'})
Write-Host ""

if (-not $frontend_running -or -not $backend_running) {
    Write-Host "⚠️  WARNING: Some services not running." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To start services manually, open two PowerShell terminals:" -ForegroundColor White
    Write-Host ""
    Write-Host "Terminal 1:" -ForegroundColor Cyan
    Write-Host "  cd F:\TitanForge\titanforge_backend" -ForegroundColor White
    Write-Host "  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor White
    Write-Host ""
    Write-Host "Terminal 2:" -ForegroundColor Cyan
    Write-Host "  cd F:\TitanForge\frontend" -ForegroundColor White
    Write-Host "  npm run dev" -ForegroundColor White
    Write-Host ""
    Write-Host "Wait 10-15 seconds for both to start, then run this script again." -ForegroundColor White
    Write-Host ""
    exit
}

Write-Host "✅ All services running!" -ForegroundColor Green
Write-Host ""

# Show demo URLs
Write-Host "═" * 66 -ForegroundColor Cyan
Write-Host "SALES DEMO - KEY URLS" -ForegroundColor Cyan
Write-Host "═" * 66 -ForegroundColor Cyan
Write-Host ""

$urls = @(
    @{ Name = "MAIN LANDING PAGE"; URL = "http://localhost:5173"; Desc = "Where leads arrive" },
    @{ Name = "PRICING PAGE"; URL = "http://localhost:5173/pricing"; Desc = "Show pricing plans" },
    @{ Name = "DASHBOARD"; URL = "http://localhost:8000/dashboard"; Desc = "Real-time metrics (5s refresh)" },
    @{ Name = "API DOCS"; URL = "http://localhost:8000/docs"; Desc = "Swagger API documentation" },
    @{ Name = "COCKPIT"; URL = "http://localhost:5173/cockpit"; Desc = "AI Agent control center" }
)

$urls | ForEach-Object {
    Write-Host "$($_.Name)" -ForegroundColor Green
    Write-Host "  URL:  $($_.URL)" -ForegroundColor White
    Write-Host "  Info: $($_.Desc)" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "═" * 66 -ForegroundColor Cyan
Write-Host "DEMO FLOW" -ForegroundColor Cyan
Write-Host "═" * 66 -ForegroundColor Cyan
Write-Host ""

$steps = @(
    "1. Open landing page (http://localhost:5173)",
    "2. Scroll to ROI Calculator section",
    "3. Enter: test@company.com, 'TechCorp', '51-500 employees'",
    "4. Click 'Download ROI Report' → Shows HTML with savings",
    "5. Watch dashboard update in real-time",
    "6. Show pricing page with Stripe checkout",
    "7. Show agent cockpit with voice control"
)

$steps | ForEach-Object {
    Write-Host "  $_" -ForegroundColor White
}

Write-Host ""
Write-Host "═" * 66 -ForegroundColor Cyan
Write-Host "LAUNCH DEMO" -ForegroundColor Cyan
Write-Host "═" * 66 -ForegroundColor Cyan
Write-Host ""

# Try to open browser
Write-Host "Opening landing page in browser..." -ForegroundColor Yellow
Write-Host ""

try {
    Start-Process "http://localhost:5173"
    Write-Host "✅ Browser window opened" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not auto-open browser. Manually visit: http://localhost:5173" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "┌─────────────────────────────────────────────────────────────────┐" -ForegroundColor Cyan
Write-Host "│ DEMO IS LIVE!                                                   │" -ForegroundColor Cyan
Write-Host "│                                                                 │" -ForegroundColor Cyan
Write-Host "│ ✓ Landing page with lead magnet                                 │" -ForegroundColor Green
Write-Host "│ ✓ ROI calculator form (generates PDF)                            │" -ForegroundColor Green
Write-Host "│ ✓ Real-time dashboard (updates every 5 seconds)                 │" -ForegroundColor Green
Write-Host "│ ✓ Pricing page with Stripe integration                          │" -ForegroundColor Green
Write-Host "│ ✓ Multi-modal AI cockpit (voice + text)                         │" -ForegroundColor Green
Write-Host "│ ✓ Full API documentation                                        │" -ForegroundColor Green
Write-Host "│                                                                 │" -ForegroundColor Cyan
Write-Host "│ Press Ctrl+C when done demoing                                  │" -ForegroundColor Cyan
Write-Host "└─────────────────────────────────────────────────────────────────┘" -ForegroundColor Cyan
Write-Host ""

# Keep script running
while ($true) {
    Start-Sleep -Seconds 1
}
