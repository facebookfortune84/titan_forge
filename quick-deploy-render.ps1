# ============================================================================
# TitanForge Render Quick Deploy
# Ultra-fast deployment (copy your credentials and go!)
# ============================================================================

# SET YOUR CREDENTIALS HERE (then run the script):
$RENDER_API_KEY = "your-render-api-key-here"
$RENDER_FRONTEND_SERVICE_ID = "your-frontend-service-id"
$RENDER_BACKEND_SERVICE_ID = "your-backend-service-id"

# ============================================================================
# OR: Pass credentials as parameters when running script:
# ============================================================================
# .\quick-deploy-render.ps1 -ApiKey "rnd_xxxxx" -FrontendId "srv-xxxxx" -BackendId "srv-xxxxx"

param(
    [string]$ApiKey = $RENDER_API_KEY,
    [string]$FrontendId = $RENDER_FRONTEND_SERVICE_ID,
    [string]$BackendId = $RENDER_BACKEND_SERVICE_ID,
    [string]$Environment = "production"
)

Write-Host @"
╔════════════════════════════════════════════════════════════════════╗
║          TitanForge Quick Render Deploy                            ║
║                                                                    ║
║  Ultra-fast one-command deployment to Render                      ║
╚════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# ============================================================================
# VALIDATION
# ============================================================================

if ([string]::IsNullOrEmpty($ApiKey) -or $ApiKey -eq "your-render-api-key-here") {
    Write-Host @"
⚠️  CREDENTIALS MISSING

HOW TO GET YOUR CREDENTIALS:

1. API KEY:
   - Go to render.com → Dashboard
   - Click avatar → Settings
   - API Keys section → Create
   - Copy the key (starts with 'rnd_')

2. SERVICE IDs:
   - Go to render.com → Dashboard
   - Click on each service (backend, frontend)
   - Look at URL: https://dashboard.render.com/web/srv-xxxxx
   - Copy the 'srv-xxxxx' part

3. RUN WITH YOUR CREDENTIALS:
   `$env:RENDER_API_KEY='rnd_xxxxx'
   `$env:RENDER_FRONTEND_SERVICE_ID='srv-xxxxx'
   `$env:RENDER_BACKEND_SERVICE_ID='srv-xxxxx'
   .\quick-deploy-render.ps1

Or edit this script and put credentials at the top.

"@ -ForegroundColor Yellow
    exit 1
}

if ([string]::IsNullOrEmpty($FrontendId) -or $FrontendId -eq "your-frontend-service-id") {
    Write-Host "⚠️  Frontend Service ID missing" -ForegroundColor Yellow
    exit 1
}

if ([string]::IsNullOrEmpty($BackendId) -or $BackendId -eq "your-backend-service-id") {
    Write-Host "⚠️  Backend Service ID missing" -ForegroundColor Yellow
    exit 1
}

# ============================================================================
# DEPLOYMENT
# ============================================================================

Write-Host "✅ Credentials found. Starting deployment..." -ForegroundColor Green

$Headers = @{
    "Authorization" = "Bearer $ApiKey"
    "Content-Type" = "application/json"
}

$Body = @{"clearCache" = "clear"} | ConvertTo-Json

# Deploy Backend
Write-Host "`n🚀 Deploying Backend..." -ForegroundColor Yellow
try {
    $Response = Invoke-WebRequest `
        -Uri "https://api.render.com/v1/services/$BackendId/deploys" `
        -Method POST `
        -Headers $Headers `
        -Body $Body `
        -ErrorAction Stop
    
    Write-Host "✅ Backend deployment triggered" -ForegroundColor Green
    $BackendDeploy = $Response.Content | ConvertFrom-Json
    Write-Host "   ID: $($BackendDeploy.id)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Backend deployment failed: $_" -ForegroundColor Red
}

# Deploy Frontend
Write-Host "`n🚀 Deploying Frontend..." -ForegroundColor Yellow
try {
    $Response = Invoke-WebRequest `
        -Uri "https://api.render.com/v1/services/$FrontendId/deploys" `
        -Method POST `
        -Headers $Headers `
        -Body $Body `
        -ErrorAction Stop
    
    Write-Host "✅ Frontend deployment triggered" -ForegroundColor Green
    $FrontendDeploy = $Response.Content | ConvertFrom-Json
    Write-Host "   ID: $($FrontendDeploy.id)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Frontend deployment failed: $_" -ForegroundColor Red
}

# Get Service URLs
Write-Host "`n🔍 Getting service URLs..." -ForegroundColor Yellow
try {
    $BackendService = Invoke-WebRequest `
        -Uri "https://api.render.com/v1/services/$BackendId" `
        -Headers @{"Authorization" = "Bearer $ApiKey"} `
        -ErrorAction Stop | ConvertFrom-Json
    
    $FrontendService = Invoke-WebRequest `
        -Uri "https://api.render.com/v1/services/$FrontendId" `
        -Headers @{"Authorization" = "Bearer $ApiKey"} `
        -ErrorAction Stop | ConvertFrom-Json
    
    Write-Host @"

╔════════════════════════════════════════════════════════════════════╗
║                   ✅ DEPLOYMENT COMPLETE                           ║
║                                                                    ║
║  Your services are deploying to Render                            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

🌐 FRONTEND:
   https://$($FrontendService.name).onrender.com

🔌 BACKEND:
   https://$($BackendService.name).onrender.com
   Health: https://$($BackendService.name).onrender.com/api/v1/health

📊 DASHBOARD:
   https://dashboard.render.com/web/

⏱️  Deployment takes 2-3 minutes. Check the dashboard for status.

"@ -ForegroundColor Green
    
} catch {
    Write-Host "⚠️  Could not retrieve service details" -ForegroundColor Yellow
}

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Wait 2-3 minutes for deployment to complete"
Write-Host "2. Test frontend: Visit the URL above"
Write-Host "3. Test backend: curl https://[backend-url]/api/v1/health"
Write-Host "4. Start marketing push"
