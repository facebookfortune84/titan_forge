# 🚀 Render Deployment – Quick Setup

## What is Render?
Render is a modern cloud platform with:
- ✅ Free tier (both frontend + backend)
- ✅ Auto-deploy from GitHub
- ✅ No credit card required
- ✅ PostgreSQL + Redis included
- ✅ Perfect for launching today

---

## FASTEST DEPLOYMENT (5 Minutes)

### Step 1: Create Render Account (1 min)
```
1. Go to render.com
2. Sign up with GitHub (easiest)
3. Click "Create new" → select type (see below)
```

### Step 2: Deploy Backend (2 min)

**Create Web Service:**
1. Click "New +" → "Web Service"
2. Connect your GitHub repo (TitanForge)
3. Set name: `titanforge-backend`
4. Choose runtime: **Python 3.12**
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn titanforge_backend.app.main:app --host 0.0.0.0 --port 8000`
7. Set environment variables:
   ```
   DATABASE_URL = postgresql://...
   REDIS_URL = redis://...
   STRIPE_SECRET_KEY = sk_test_...
   ```
8. Click "Create Web Service"

**⏱️ Deployment takes ~2-3 minutes**

### Step 3: Deploy Frontend (1 min)

**Create Static Site:**
1. Click "New +" → "Static Site"
2. Connect your GitHub repo (same repo)
3. Set name: `titanforge-frontend`
4. Build command: `cd frontend && npm run build`
5. Publish directory: `frontend/dist`
6. Click "Create Static Site"

**⏱️ Deployment takes ~1-2 minutes**

### Step 4: Get Your URLs
```
Frontend: https://titanforge-frontend.onrender.com
Backend: https://titanforge-backend.onrender.com/api/v1/health
```

---

## COMMAND-LINE DEPLOYMENT (1 Command)

### Setup (One Time Only)

```powershell
# 1. Create API key at render.com:
#    Settings → API Keys → Create New

# 2. Set environment variables (PowerShell):
[Environment]::SetEnvironmentVariable('RENDER_API_KEY', 'rnd_xxxxxxxxxxxxxxx', 'User')
[Environment]::SetEnvironmentVariable('RENDER_FRONTEND_SERVICE_ID', 'srv-xxxxx', 'User')
[Environment]::SetEnvironmentVariable('RENDER_BACKEND_SERVICE_ID', 'srv-xxxxx', 'User')

# 3. Restart PowerShell
```

**Find your Service IDs:**
- Go to render.com dashboard
- Click on your service
- URL = `https://dashboard.render.com/web/srv-xxxxx`
- Copy the `srv-xxxxx` part

### Deploy (Every Time)

```powershell
# Deploy both frontend and backend
.\deploy-render.ps1

# Or deploy just backend
.\deploy-render.ps1 -BackendOnly

# Or deploy just frontend  
.\deploy-render.ps1 -FrontendOnly

# Skip build (if no changes)
.\deploy-render.ps1 -SkipBuild
```

**That's it! One command to deploy everything.**

---

## AUTOMATIC DEPLOYMENT (Even Easier)

Render can auto-deploy when you push to GitHub:

1. In Render dashboard, go to your service
2. Settings → "Auto-Deploy" → Enable
3. Now every `git push` automatically deploys ✅

```bash
git add --all
git commit -m "Deploy latest"
git push origin main
# ✅ Automatically deploys to Render!
```

---

## DATABASE SETUP (If Needed)

### PostgreSQL
```
Render auto-creates for you OR:
1. Click "New +" → "PostgreSQL"
2. Select free tier
3. Copy connection string to backend env vars
```

### Redis
```
Render auto-creates for you OR:
1. Click "New +" → "Redis"
2. Select free tier  
3. Copy connection string to backend env vars
```

---

## ENVIRONMENT VARIABLES (Backend)

Create in Render dashboard → Service → Environment:

```
DATABASE_URL = postgresql://user:password@host/dbname
REDIS_URL = redis://default:password@host:6379
STRIPE_SECRET_KEY = sk_test_xxxxxxx
STRIPE_PUBLIC_KEY = pk_test_xxxxxxx
STRIPE_WEBHOOK_SECRET = whsec_xxxxxxx
JWT_SECRET = your-secret-key
ENVIRONMENT = production
```

---

## TROUBLESHOOTING

### Frontend not building?
```
Check build command:
cd frontend && npm run build

Common fixes:
- npm install
- Clear node_modules and reinstall
- Check TypeScript errors (npm run build outputs them)
```

### Backend crashing?
```
Check logs in Render dashboard:
1. Go to service
2. Logs tab
3. Look for error messages

Common fixes:
- Missing database URL env var
- Missing STRIPE keys
- Port not set to 8000
```

### How do I see logs?
```
Render Dashboard:
1. Select service
2. Click "Logs" tab
3. Real-time logs appear

Or PowerShell:
render logs [service-id]
```

### How do I redeploy?
```
# Option A: Push to GitHub (auto-deploys)
git push origin main

# Option B: Manual trigger
.\deploy-render.ps1

# Option C: Render dashboard
Click "Deploy" button on service page
```

---

## COST

**Free tier includes:**
- ✅ 2 web services (or 1 web + 1 static)
- ✅ 0.5 CPU + 512 MB RAM
- ✅ 1 PostgreSQL database (90 days retention)
- ✅ 1 Redis instance (25 MB)
- ✅ 100 GB bandwidth/month
- ✅ Free SSL certificates

**When to upgrade:**
- Need more resources (scale from $7/month)
- Need production SLA (from $12/month)
- Need custom domain (already included on free)

---

## NEXT STEPS

### Option A: Quick Setup (5 min, manual)
1. Go to render.com
2. Create account
3. Follow "Fastest Deployment" steps above
4. Get your URLs
5. Done!

### Option B: Command-Line (1 min after setup)
1. Follow "Setup" steps once
2. Run `.\deploy-render.ps1`
3. Done!

### Option C: Full Auto (Git push)
1. Enable "Auto-Deploy" in Render
2. `git push origin main`
3. Automatically deploys!
4. Done!

---

## VERIFY DEPLOYMENT

```bash
# Check frontend
curl https://titanforge-frontend.onrender.com

# Check backend health
curl https://titanforge-backend.onrender.com/api/v1/health

# Both should return data (not 404 or 500)
```

---

## FAQ

**Q: Can I use a custom domain?**  
A: Yes, add it in Render dashboard (Settings → Custom Domain)

**Q: Does my data persist?**  
A: Yes, PostgreSQL and Redis persist automatically

**Q: Can I scale up later?**  
A: Yes, anytime. Just change plan (2-5 min redeploy)

**Q: Do I need Docker?**  
A: No, Render handles everything

**Q: Is it production-ready?**  
A: Yes, perfect for MVP and production use

---

## ONE-LINER DEPLOYMENT

```powershell
# Deploy everything in one command:
.\deploy-render.ps1 -SkipBuild $false

# Or if already built:
git add --all && git commit -m "Deploy" && git push origin main
```

That's it! 🚀

---

*For more details, see: https://render.com/docs*
