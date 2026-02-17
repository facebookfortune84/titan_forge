# ============================================================================
# Switch Vercel Account & Deploy to Custom Domain
# ============================================================================

param(
    [string]$Domain = "www.realmstoriches.xyz",
    [switch]$SkipBuild = $false
)

Write-Host @"
╔════════════════════════════════════════════════════════════════════╗
║          Switch Vercel Account & Deploy to Custom Domain           ║
║                                                                    ║
║  Domain: $Domain
╚════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# ============================================================================
# STEP 1: Build Frontend
# ============================================================================

if (-not $SkipBuild) {
    Write-Host "`n🔨 Building frontend..." -ForegroundColor Yellow
    try {
        cd frontend
        npm run build
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Build failed" -ForegroundColor Red
            cd ..
            exit 1
        }
        
        Write-Host "✅ Frontend built" -ForegroundColor Green
        cd ..
    } catch {
        Write-Host "❌ Build error: $_" -ForegroundColor Red
        cd ..
        exit 1
    }
}

# ============================================================================
# STEP 2: Sign Out of Current Account
# ============================================================================

Write-Host "`n🔐 Current Vercel account:" -ForegroundColor Yellow
vercel whoami

Write-Host "`n❓ Do you want to switch to a different account?" -ForegroundColor Yellow
Write-Host "   Press Y to logout and sign into different account" -ForegroundColor Gray
Write-Host "   Press N to continue with current account" -ForegroundColor Gray

$response = Read-Host "Switch account? (Y/N)"

if ($response -eq "Y" -or $response -eq "y") {
    Write-Host "`n🚪 Logging out..." -ForegroundColor Yellow
    vercel logout
    
    Write-Host "`n🔑 Now signing in with new account..." -ForegroundColor Yellow
    Write-Host "   (Browser will open - authorize with your account)" -ForegroundColor Gray
    vercel login
    
    Write-Host "`n✅ Logged in as:" -ForegroundColor Green
    vercel whoami
}

# ============================================================================
# STEP 3: Deploy to Vercel
# ============================================================================

Write-Host "`n🚀 Deploying to Vercel..." -ForegroundColor Yellow

cd frontend

# Deploy
$deployOutput = vercel deploy --prod 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend deployed!" -ForegroundColor Green
    Write-Host $deployOutput
} else {
    Write-Host "⚠️  Deployment output:" -ForegroundColor Yellow
    Write-Host $deployOutput
}

cd ..

# ============================================================================
# STEP 4: Add Custom Domain
# ============================================================================

Write-Host "`n🌐 Adding custom domain: $Domain" -ForegroundColor Yellow
Write-Host "   (You may need to update DNS at your registrar)" -ForegroundColor Gray

cd frontend

# Add domain
vercel domains add $Domain

Write-Host "`n📋 Domain setup instructions:" -ForegroundColor Yellow
Write-Host "   1. Vercel will show you the DNS records to add" -ForegroundColor Gray
Write-Host "   2. Go to your domain registrar (where you bought www.realmstoriches.xyz)" -ForegroundColor Gray
Write-Host "   3. Add the DNS records Vercel shows" -ForegroundColor Gray
Write-Host "   4. Wait 5-30 minutes for DNS to propagate" -ForegroundColor Gray
Write-Host "   5. Visit https://$Domain - should see your landing page!" -ForegroundColor Gray

cd ..

# ============================================================================
# SUMMARY
# ============================================================================

Write-Host @"

╔════════════════════════════════════════════════════════════════════╗
║                   ✅ DEPLOYMENT COMPLETE                           ║
║                                                                    ║
║  Your frontend is deployed and connected to your domain            ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

🌐 Your URLs:
   Vercel URL: https://titanforge-frontend.vercel.app
   Custom Domain: https://$Domain (after DNS setup)

📍 NEXT STEPS:

1. Copy the DNS records from the Vercel output above

2. Go to your domain registrar:
   - GoDaddy: Manage Domain → DNS Records
   - Namecheap: Domain List → Manage DNS
   - Google Domains: DNS settings
   - Or wherever you registered realmstoriches.xyz

3. Add the CNAME/A records Vercel showed you

4. Wait 5-30 minutes (DNS propagation)

5. Visit: https://$Domain

💡 TIP: You can use the Vercel URL immediately while DNS is updating:
   https://titanforge-frontend.vercel.app

📚 Help:
   - Vercel domain guide: https://vercel.com/docs/concepts/projects/domains
   - DNS propagation checker: https://www.whatsmydns.net

"@ -ForegroundColor Green
