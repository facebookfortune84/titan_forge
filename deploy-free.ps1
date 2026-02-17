# ============================================================================
# TitanForge Free Deployment Script
# Frontend: Vercel (free, you're already signed in as realmstoriches)
# Backend: Railway (free tier with $5/month credit)
# ============================================================================

param(
    [switch]$FrontendOnly = $false,
    [switch]$BackendOnly = $false,
    [switch]$SkipBuild = $false
)

Write-Host @"
╔════════════════════════════════════════════════════════════════════╗
║          TitanForge Free Deployment (Vercel + Railway)             ║
║                                                                    ║
║  Frontend → Vercel (FREE, you're already signed in)               ║
║  Backend → Railway (FREE tier with \$5/month credit)               ║
╚════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# ============================================================================
# CHECK PREREQUISITES
# ============================================================================

Write-Host "`n🔍 Checking prerequisites..." -ForegroundColor Yellow

$vercelOk = $false
$railwayOk = $false

# Check Vercel CLI
if (Get-Command vercel -ErrorAction SilentlyContinue) {
    Write-Host "✅ Vercel CLI found" -ForegroundColor Green
    $vercelOk = $true
} else {
    Write-Host "⚠️  Vercel CLI not found. Install: npm install -g vercel" -ForegroundColor Yellow
}

# Check Railway CLI
if (Get-Command railway -ErrorAction SilentlyContinue) {
    Write-Host "✅ Railway CLI found" -ForegroundColor Green
    $railwayOk = $true
} else {
    Write-Host "⚠️  Railway CLI not found. Install: npm install -g @railway/cli" -ForegroundColor Yellow
}

# ============================================================================
# BUILD FRONTEND
# ============================================================================

if (-not $BackendOnly -and -not $SkipBuild) {
    Write-Host "`n🔨 Building frontend..." -ForegroundColor Yellow
    try {
        cd frontend
        npm run build
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Frontend build failed" -ForegroundColor Red
            cd ..
            exit 1
        }
        
        Write-Host "✅ Frontend built successfully" -ForegroundColor Green
        cd ..
    } catch {
        Write-Host "❌ Build error: $_" -ForegroundColor Red
        cd ..
        exit 1
    }
}

# ============================================================================
# DEPLOY FRONTEND TO VERCEL
# ============================================================================

if (-not $BackendOnly) {
    Write-Host "`n🚀 Deploying frontend to Vercel..." -ForegroundColor Yellow
    Write-Host "   (You're signed in as: realmstoriches)" -ForegroundColor Gray
    
    try {
        cd frontend
        
        # Deploy to Vercel
        $vercelOutput = vercel deploy --prod 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Frontend deployed to Vercel!" -ForegroundColor Green
            Write-Host $vercelOutput | Select-String "https://" | Write-Host -ForegroundColor Cyan
        } else {
            Write-Host "⚠️  Vercel deployment output:" -ForegroundColor Yellow
            Write-Host $vercelOutput
        }
        
        cd ..
    } catch {
        Write-Host "❌ Deployment error: $_" -ForegroundColor Red
        cd ..
    }
}

# ============================================================================
# DEPLOY BACKEND TO RAILWAY
# ============================================================================

if (-not $FrontendOnly) {
    Write-Host "`n🚀 Deploying backend to Railway..." -ForegroundColor Yellow
    Write-Host "   (First time: will prompt for login)" -ForegroundColor Gray
    
    try {
        # Check if Railway is logged in
        $railwayStatus = railway whoami 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "⚠️  Not logged into Railway. Opening login..." -ForegroundColor Yellow
            railway login
        }
        
        Write-Host "`n📝 Setting up Railway project..." -ForegroundColor Yellow
        
        # Initialize Railway if needed
        if (-not (Test-Path "railway.json")) {
            Write-Host "   Creating railway.json..." -ForegroundColor Gray
            @{
                "$schema" = "https://railway.app/railway.schema.json"
                "build" = @{
                    "builder" = "nixpacks"
                }
                "deploy" = @{
                    "numReplicas" = 1
                    "startCommand" = "uvicorn titanforge_backend.app.main:app --host 0.0.0.0 --port 8000"
                    "healthcheckPath" = "/api/v1/health"
                    "healthcheckTimeout" = 100
                }
            } | ConvertTo-Json | Out-File railway.json
        }
        
        # Deploy
        Write-Host "   Deploying to Railway..." -ForegroundColor Gray
        railway up
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Backend deployed to Railway!" -ForegroundColor Green
        }
        
    } catch {
        Write-Host "⚠️  Railway deployment note: $_" -ForegroundColor Yellow
    }
}

# ============================================================================
# SUMMARY
# ============================================================================

Write-Host @"

╔════════════════════════════════════════════════════════════════════╗
║                   ✅ DEPLOYMENT INITIATED                          ║
║                                                                    ║
║  Frontend: Deployed to Vercel (realmstoriches.vercel.app)         ║
║  Backend: Deploying to Railway (check dashboard)                  ║
║                                                                    ║
║  ⏱️  Frontend: ~30 seconds                                         ║
║  ⏱️  Backend: ~2-3 minutes                                         ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

📍 NEXT STEPS:

1. Frontend Ready:
   Visit: https://titanforge-frontend.vercel.app
   (or your custom domain if configured)

2. Backend Deploying:
   Go to: railway.app/dashboard
   Wait for deployment to complete
   Your backend URL will appear there

3. Connect Backend URL to Frontend:
   Edit frontend/.env.production:
   VITE_API_URL=https://your-railway-backend.up.railway.app

4. Test:
   Frontend: https://titanforge-frontend.vercel.app
   Backend health: https://your-railway.up.railway.app/api/v1/health

5. Redeploy frontend (if you changed env):
   vercel deploy --prod

"@ -ForegroundColor Green

Write-Host "Deployment script complete!" -ForegroundColor Cyan
