# 🚀 TITANFORGE RENDER DEPLOYMENT – CHOOSE YOUR METHOD

**Status:** Ready to deploy to Render in 5 minutes  
**Options:** Manual (GUI) or Command-line  
**Effort:** ~5 minutes setup, then 1 command forever  

---

## 🎯 QUICK START – PICK ONE METHOD

### METHOD 1: Fastest (5 min, GUI only) ⚡

Perfect if: You want it live RIGHT NOW, don't care about automation

```
1. Go to render.com
2. Sign up with GitHub
3. Click "New" → Create 2 services:
   - Web Service (backend)
   - Static Site (frontend)
4. Paste settings (see guide below)
5. Done! Both live in 2-3 minutes
```

**Link to full guide:** See "Manual GUI Deployment" below

---

### METHOD 2: Recommended (5 min setup, 1 command deploy) 💡

Perfect if: You want to deploy forever with 1 command

```powershell
# Setup (one time):
[Environment]::SetEnvironmentVariable('RENDER_API_KEY', 'rnd_xxxxx', 'User')
[Environment]::SetEnvironmentVariable('RENDER_FRONTEND_SERVICE_ID', 'srv-xxxxx', 'User')
[Environment]::SetEnvironmentVariable('RENDER_BACKEND_SERVICE_ID', 'srv-xxxxx', 'User')

# Deploy (every time):
.\deploy-render.ps1

# That's it! Both frontend and backend deploy with one command
```

---

### METHOD 3: Fully Automatic (Auto-deploy on git push) 🤖

Perfect if: You want zero manual deployment steps

```bash
# Setup in Render dashboard: Enable "Auto-Deploy"
# Then every push auto-deploys:

git add --all
git commit -m "Latest code"
git push origin main
# ✅ Automatically deploying to Render right now!
```

---

## 📋 MANUAL GUI DEPLOYMENT (Method 1)

### Step 1: Create Render Account (1 min)
1. Go to **render.com**
2. Click "Sign up"
3. Choose "Continue with GitHub" (easiest)
4. Authorize GitHub access
5. Done

### Step 2: Deploy Backend as Web Service (2 min)

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Select your TitanForge GitHub repo
3. Fill in settings:

```
Name:              titanforge-backend
Environment:       Python 3
Region:            Oregon (closest to you)
Branch:            main
Build Command:     pip install -r titanforge_backend/requirements.txt
Start Command:     uvicorn titanforge_backend.app.main:app --host 0.0.0.0 --port 8000
```

4. Scroll down → **"Advanced"** → Add environment variables:

```
DATABASE_URL     = postgresql://YOUR_DB_URL
REDIS_URL        = redis://YOUR_REDIS_URL
STRIPE_SECRET_KEY = sk_test_xxxxxxxxxxxxx
STRIPE_PUBLIC_KEY = pk_test_xxxxxxxxxxxxx
JWT_SECRET       = your-secret-key-here
ENVIRONMENT      = production
```

5. Click **"Create Web Service"**

**⏱️ Wait 2-3 minutes for deployment**

### Step 3: Deploy Frontend as Static Site (1 min)

1. Click **"New +"** → **"Static Site"**
2. Select your TitanForge GitHub repo (same one)
3. Fill in settings:

```
Name:               titanforge-frontend
Branch:             main
Build Command:      cd frontend && npm run build
Publish Directory:  frontend/dist
```

4. Click **"Create Static Site"**

**⏱️ Wait 1-2 minutes for deployment**

### Step 4: Get Your Live URLs

After both deploy, you'll have:

```
🌐 Frontend:  https://titanforge-frontend.onrender.com
🔌 Backend:   https://titanforge-backend.onrender.com
🏥 Health:    https://titanforge-backend.onrender.com/api/v1/health
```

**You're LIVE! 🎉**

---

## ⚡ COMMAND-LINE DEPLOYMENT (Method 2)

### One-Time Setup

#### 1. Create Render API Key

```
1. Go to render.com dashboard
2. Click your avatar → Settings
3. Find "API Keys" section
4. Click "Create"
5. Copy the key (starts with "rnd_")
```

#### 2. Find Your Service IDs

After creating services (Method 1 or Method 3):

```
For each service:
1. Go to dashboard
2. Click the service name
3. Look at the URL: https://dashboard.render.com/web/srv-xxxxxxx
4. Copy the srv-xxxxxxx part
```

#### 3. Set Environment Variables

```powershell
# Open PowerShell and run:
[Environment]::SetEnvironmentVariable('RENDER_API_KEY', 'rnd_xxxxxxxxxxxxx', 'User')
[Environment]::SetEnvironmentVariable('RENDER_FRONTEND_SERVICE_ID', 'srv-xxxxx', 'User')
[Environment]::SetEnvironmentVariable('RENDER_BACKEND_SERVICE_ID', 'srv-xxxxx', 'User')

# Close and reopen PowerShell for changes to take effect
```

### Deploy with One Command

```powershell
# Navigate to project root
cd F:\TitanForge

# Run deployment script
.\deploy-render.ps1

# Script will:
# 1. Build frontend (npm run build)
# 2. Build backend (python syntax check)
# 3. Git commit + push
# 4. Trigger Render deployments
# 5. Show you live URLs

# Total time: ~60 seconds
```

---

## 🤖 AUTOMATIC DEPLOYMENT (Method 3)

### Enable Auto-Deploy

```
1. Go to Render dashboard
2. Click on your service (backend or frontend)
3. Go to Settings → Auto-Deploy
4. Toggle "Auto-Deploy" ON
5. Save
```

### Deploy Automatically

```bash
# Now every git push auto-deploys!

git add --all
git commit -m "Deploy latest changes"
git push origin main

# Render detects push and auto-deploys immediately
# ✅ Your app is updating without you doing anything
```

---

## 📊 COMPARISON

| Feature | GUI (1) | CLI (2) | Auto (3) |
|---------|---------|---------|----------|
| Setup time | 5 min | 5 min | 5 min |
| Deploy time | 2-3 min | 60 sec | Auto |
| Each deploy | Click "Deploy" | 1 command | Just git push |
| Complexity | Low | Low | Very Low |
| Best for | One-time | Frequent deploys | Continuous |

---

## 🔄 TYPICAL WORKFLOW

### CLI Method (Recommended for Today)

```powershell
# Morning: Make changes to code
# Evening: Deploy with one command

.\deploy-render.ps1

# Outputs:
# ✅ Frontend built
# ✅ Backend ready
# ✅ Pushed to GitHub  
# ✅ Render deploying...
# 
# Frontend: https://titanforge-frontend.onrender.com
# Backend:  https://titanforge-backend.onrender.com/api/v1/health
```

### Auto Method (Later)

```bash
# Just push code, everything else is automatic

git push origin main
# ✅ Automatically deploying to Render...
# Done! Your latest code is live
```

---

## ✅ VERIFY IT WORKS

After deployment, test:

```bash
# Test frontend loads
curl https://titanforge-frontend.onrender.com
# Should return HTML

# Test backend is responding
curl https://titanforge-backend.onrender.com/api/v1/health
# Should return: {"status": "healthy"}

# Test payment endpoint
curl https://titanforge-backend.onrender.com/api/v1/pricing
# Should return pricing data
```

---

## 🆘 TROUBLESHOOTING

### Build Failed?
```
Check Render logs:
1. Dashboard → Service → Logs
2. Look for error messages
3. Common: Missing env vars, bad build command
```

### Service won't start?
```
1. Check environment variables are set
2. Check database URL is correct
3. Check Redis URL is correct
4. Restart service: Dashboard → "Reboot"
```

### Getting 404 errors?
```
Frontend: Make sure publish directory is "frontend/dist"
Backend: Make sure start command includes port 8000
```

---

## 💡 TIPS

**Redeploy faster:**
- Use CLI method: `.\deploy-render.ps1` (60 seconds)
- Or auto-deploy: just push (automatic)

**Monitor deployment:**
- Watch Render dashboard Logs tab in real-time
- Or use: `render logs [service-id]`

**Scale later:**
- Render lets you upgrade instantly
- Go from free to paid: $7/month for extra resources

**Custom domain:**
- Render dashboard → Settings → Custom Domain
- Add your domain (takes ~5 min to propagate)

---

## 🎯 YOUR NEXT STEP

### Choose your method:

**Want to deploy RIGHT NOW? (5 min)**
→ Use Method 1 (GUI) - See "Manual GUI Deployment" above

**Want 1-command deploy? (Setup once, then fast)**
→ Use Method 2 (CLI) - Follow "Command-Line Deployment" above

**Want fully automatic? (Zero manual steps)**
→ Use Method 3 (Auto) - Enable in Render dashboard

---

## 📚 FULL GUIDES

- **Render_Deployment_Guide.md** – Detailed instructions
- **deploy-render.ps1** – Deployment script
- **HYBRID_LAUNCH_READY.md** – Full launch plan

---

**Ready to launch?**

Pick your method → Follow steps → Get your live URLs → Start selling!

🚀
