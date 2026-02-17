# ============================================================================
# TitanForge Render Deployment Script
# One-command deployment for both frontend and backend to Render
# ============================================================================

param(
    [string]$Environment = "production",
    [switch]$SkipBuild = $false,
    [switch]$BackendOnly = $false,
    [switch]$FrontendOnly = $false
)

Write-Host @"
╔════════════════════════════════════════════════════════════════════╗
║          TitanForge Render Deployment Script                       ║
║                                                                    ║
║  Deploy both frontend and backend to Render with one command      ║
╚════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# ============================================================================
# CONFIGURATION
# ============================================================================

$FRONTEND_SERVICE_ID = $env:RENDER_FRONTEND_SERVICE_ID  # Set as env var
$BACKEND_SERVICE_ID = $env:RENDER_BACKEND_SERVICE_ID    # Set as env var
$RENDER_API_KEY = $env:RENDER_API_KEY                   # Set as env var

# Validate credentials
if ([string]::IsNullOrEmpty($RENDER_API_KEY)) {
    Write-Host @"
⚠️  ERROR: Missing Render API credentials

Setup instructions:
1. Create account at render.com
2. Create API key: Settings → API Keys → Create
3. Set environment variables:
   
   On Windows PowerShell:
   [Environment]::SetEnvironmentVariable('RENDER_API_KEY', 'your-key', 'User')
   [Environment]::SetEnvironmentVariable('RENDER_FRONTEND_SERVICE_ID', 'srv-xxxxx', 'User')
   [Environment]::SetEnvironmentVariable('RENDER_BACKEND_SERVICE_ID', 'srv-xxxxx', 'User')
   
   Then restart PowerShell.

Or run once with credentials:
   `$env:RENDER_API_KEY='your-key'; `$env:RENDER_FRONTEND_SERVICE_ID='srv-xxxxx'; .\deploy-render.ps1

"@ -ForegroundColor Red
    exit 1
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

function Deploy-Service {
    param(
        [string]$ServiceId,
        [string]$ServiceName
    )
    
    Write-Host "`n🚀 Deploying $ServiceName..." -ForegroundColor Yellow
    
    $Headers = @{
        "Authorization" = "Bearer $RENDER_API_KEY"
        "Content-Type" = "application/json"
    }
    
    $Body = @{
        "clearCache" = "clear"
    } | ConvertTo-Json
    
    try {
        $Response = Invoke-WebRequest `
            -Uri "https://api.render.com/v1/services/$ServiceId/deploys" `
            -Method POST `
            -Headers $Headers `
            -Body $Body `
            -ErrorAction Stop
        
        Write-Host "✅ $ServiceName deployment triggered" -ForegroundColor Green
        Write-Host "   Service ID: $ServiceId" -ForegroundColor Gray
        return $true
    } catch {
        Write-Host "❌ Failed to deploy $ServiceName" -ForegroundColor Red
        Write-Host "   Error: $_" -ForegroundColor Red
        return $false
    }
}

function Build-Frontend {
    Write-Host "`n🔨 Building frontend..." -ForegroundColor Yellow
    
    try {
        cd frontend
        npm run build
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Frontend build failed" -ForegroundColor Red
            cd ..
            return $false
        }
        
        Write-Host "✅ Frontend built successfully" -ForegroundColor Green
        cd ..
        return $true
    } catch {
        Write-Host "❌ Build error: $_" -ForegroundColor Red
        cd ..
        return $false
    }
}

function Build-Backend {
    Write-Host "`n🔨 Building backend..." -ForegroundColor Yellow
    
    try {
        cd titanforge_backend
        # Backend is Python - just verify it works
        python -m py_compile main.py
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Backend syntax check failed" -ForegroundColor Red
            cd ..
            return $false
        }
        
        Write-Host "✅ Backend syntax check passed" -ForegroundColor Green
        cd ..
        return $true
    } catch {
        Write-Host "❌ Build error: $_" -ForegroundColor Red
        cd ..
        return $false
    }
}

function Verify-Deployments {
    Write-Host "`n🔍 Verifying deployments..." -ForegroundColor Yellow
    
    $Headers = @{
        "Authorization" = "Bearer $RENDER_API_KEY"
    }
    
    # Check frontend
    if (-not [string]::IsNullOrEmpty($FRONTEND_SERVICE_ID)) {
        try {
            $Response = Invoke-WebRequest `
                -Uri "https://api.render.com/v1/services/$FRONTEND_SERVICE_ID" `
                -Headers $Headers `
                -ErrorAction Stop
            
            $Service = $Response | ConvertFrom-Json
            Write-Host "Frontend: https://$($Service.name).onrender.com" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  Could not verify frontend" -ForegroundColor Yellow
        }
    }
    
    # Check backend
    if (-not [string]::IsNullOrEmpty($BACKEND_SERVICE_ID)) {
        try {
            $Response = Invoke-WebRequest `
                -Uri "https://api.render.com/v1/services/$BACKEND_SERVICE_ID" `
                -Headers $Headers `
                -ErrorAction Stop
            
            $Service = $Response | ConvertFrom-Json
            Write-Host "Backend: https://$($Service.name).onrender.com/api/v1/health" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  Could not verify backend" -ForegroundColor Yellow
        }
    }
}

# ============================================================================
# MAIN DEPLOYMENT FLOW
# ============================================================================

$StartTime = Get-Date
$Success = $true

try {
    # Step 1: Build
    if (-not $SkipBuild) {
        if (-not $BackendOnly) {
            if (-not (Build-Frontend)) {
                $Success = $false
            }
        }
        
        if (-not $FrontendOnly) {
            if (-not (Build-Backend)) {
                $Success = $false
            }
        }
    }
    
    if (-not $Success) {
        Write-Host "`n❌ Build failed. Fix errors and try again." -ForegroundColor Red
        exit 1
    }
    
    # Step 2: Git commit
    Write-Host "`n📝 Committing changes..." -ForegroundColor Yellow
    git add --all
    $CommitMessage = "Deploy to Render: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    git commit -m $CommitMessage -q
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  No changes to commit (that's OK)" -ForegroundColor Gray
    }
    
    # Step 3: Push to GitHub (Render will auto-deploy)
    Write-Host "`n🔄 Pushing to GitHub..." -ForegroundColor Yellow
    git push origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Pushed to GitHub (Render will auto-deploy)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Push failed or no changes" -ForegroundColor Yellow
    }
    
    # Step 4: Trigger manual deployments (if needed)
    Write-Host "`n🚀 Triggering Render deployments..." -ForegroundColor Yellow
    
    if (-not $FrontendOnly) {
        Deploy-Service -ServiceId $BACKEND_SERVICE_ID -ServiceName "Backend"
    }
    
    if (-not $BackendOnly) {
        Deploy-Service -ServiceId $FRONTEND_SERVICE_ID -ServiceName "Frontend"
    }
    
    # Step 5: Verify
    Verify-Deployments
    
    $EndTime = Get-Date
    $Duration = ($EndTime - $StartTime).TotalSeconds
    
    Write-Host @"

╔════════════════════════════════════════════════════════════════════╗
║                   ✅ DEPLOYMENT COMPLETE                           ║
║                                                                    ║
║  Your application is deploying to Render                          ║
║  Check your Render dashboard for live status                      ║
║                                                                    ║
║  Completed in: $([Math]::Round($Duration, 2)) seconds
╚════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Green
    
} catch {
    Write-Host "`n❌ Deployment failed: $_" -ForegroundColor Red
    exit 1
}
