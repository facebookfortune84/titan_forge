# 🚀 DEPLOY TONIGHT – COMMAND LINE READY

**Status:** Everything ready for immediate Render deployment  
**Your environment:** Variables already configured  
**Timeline:** 5 minutes to live  

---

## 🎯 IMMEDIATE ACTION (Choose One)

### Method 1: Quick Deploy Script (1 min, fully automated) ⚡

```powershell
# Set your credentials (if not already in environment):
$env:RENDER_API_KEY = 'your-api-key'
$env:RENDER_FRONTEND_SERVICE_ID = 'srv-xxxxx'
$env:RENDER_BACKEND_SERVICE_ID = 'srv-xxxxx'

# Deploy both services:
.\quick-deploy-render.ps1

# That's it! Output shows:
# ✅ Backend deployed
# ✅ Frontend deployed
# 🌐 Frontend URL: https://...onrender.com
# 🔌 Backend URL: https://...onrender.com
```

### Method 2: Manual Render GUI (5 min, most control)

1. Go to render.com
2. Sign up (use GitHub, fastest)
3. Create Web Service (backend)
   - Python 3.12
   - `pip install -r requirements.txt`
   - `uvicorn titanforge_backend.app.main:app --host 0.0.0.0 --port 8000`
4. Create Static Site (frontend)
   - `cd frontend && npm run build`
   - Publish: `frontend/dist`
5. Done!

### Method 3: Git Auto-Deploy (Zero manual, but takes 3 min setup)

```powershell
# 1. Run quick-deploy-render.ps1 once to create services

# 2. In Render dashboard, enable "Auto-Deploy"

# 3. From now on:
git add --all
git commit -m "Deploy"
git push origin main
# ✅ Automatically deploys!
```

---

## 📋 YOUR CREDENTIALS

You mentioned your environment variables are already set. Perfect!

**To verify they're loaded:**
```powershell
echo $env:RENDER_API_KEY
echo $env:RENDER_FRONTEND_SERVICE_ID
echo $env:RENDER_BACKEND_SERVICE_ID
```

**If you need to set them:**
```powershell
# PowerShell (currently running session):
$env:RENDER_API_KEY = 'rnd_xxxxxxxxxxxxx'
$env:RENDER_FRONTEND_SERVICE_ID = 'srv-xxxxx'
$env:RENDER_BACKEND_SERVICE_ID = 'srv-xxxxx'

# Permanent (all future sessions):
[Environment]::SetEnvironmentVariable('RENDER_API_KEY', 'rnd_xxxxxxxxxxxxx', 'User')
[Environment]::SetEnvironmentVariable('RENDER_FRONTEND_SERVICE_ID', 'srv-xxxxx', 'User')
[Environment]::SetEnvironmentVariable('RENDER_BACKEND_SERVICE_ID', 'srv-xxxxx', 'User')
```

---

## 🚀 HOW TO GET YOUR RENDER CREDENTIALS

### 1. API Key

```
1. Go to https://dashboard.render.com/
2. Click your avatar (top right)
3. Settings → API Keys
4. Create API Key
5. Copy the key (starts with "rnd_")
```

### 2. Service IDs

After creating your services in Render:

```
For Backend:
1. Dashboard → Web Services → Your backend service
2. Look at URL: https://dashboard.render.com/web/srv-c123...
3. Copy everything after "/web/" (srv-c123...)

For Frontend:
1. Dashboard → Static Sites → Your frontend service
2. Look at URL: https://dashboard.render.com/web/srv-f456...
3. Copy everything after "/web/" (srv-f456...)
```

---

## 📁 YOUR DEPLOYMENT FILES

**3 files ready to use:**

1. **quick-deploy-render.ps1** ← USE THIS (simplest)
   - One command deploys everything
   - Shows live URLs

2. **deploy-render.ps1** (advanced)
   - Also does git commit + push
   - More features

3. **RENDER_QUICK_START.md** (reference)
   - All 3 methods explained
   - Troubleshooting included

---

## ⏱️ WHAT HAPPENS NEXT

### When you run the script:
1. **Backend deployment triggered** (2-3 min to go live)
2. **Frontend deployment triggered** (1-2 min to go live)
3. **Your live URLs appear** in terminal

### Example output:
```
✅ Backend deployment triggered
✅ Frontend deployment triggered

🌐 FRONTEND: https://titanforge-frontend.onrender.com
🔌 BACKEND: https://titanforge-backend.onrender.com
🏥 HEALTH: https://titanforge-backend.onrender.com/api/v1/health

⏱️ Deployment takes 2-3 minutes. Check dashboard for status.
```

### After deployment:
- ✅ Your frontend is LIVE at the URL
- ✅ Your backend API is LIVE at the URL
- ✅ Payments are ready (Stripe test mode)
- ✅ Ready for customers!

---

## 🧪 VERIFY DEPLOYMENT

### Test Frontend
```bash
# Visit in browser:
https://your-frontend-url.onrender.com

# Should show landing page with:
# - Hero: "Ship Code 3x Faster with AI Agents"
# - CTA: "Get 14 Days Free"
# - Pricing section
```

### Test Backend
```bash
# Check health:
curl https://your-backend-url.onrender.com/api/v1/health

# Should return:
# {"status": "healthy", "version": "1.0"}
```

### Test Payment Flow
```
1. Visit frontend URL
2. Click "Get 14 Days Free"
3. Complete signup
4. Test payment with: 4242 4242 4242 4242
5. Should see success confirmation
```

---

## 🎯 TONIGHT'S TIMELINE

### 5 PM (Now)
- [ ] Run: `.\quick-deploy-render.ps1`
- [ ] Get live URLs
- [ ] Test end-to-end flow (10 min)

### 5:30 PM
- [ ] System is LIVE ✅
- [ ] Ready for customers

### 6-9 PM (Automation Setup)
- [ ] Email provider (SendGrid/Mailgun) - 30 min
- [ ] Zapier automation - 60 min
- [ ] Analytics setup - 30 min
- [ ] Monitoring alerts - 30 min

### 9 PM Tomorrow Morning
- [ ] Your marketing push - 4-6 hours
- [ ] Expected: 2-5 first customers by EOD

---

## 🆘 TROUBLESHOOTING

### "Service not found" error?
```
Check your Service IDs:
1. Go to render.com/dashboard
2. Verify srv-xxxxx IDs are correct
3. Retry with correct IDs
```

### "API Key invalid" error?
```
Check your API Key:
1. render.com/dashboard → Settings → API Keys
2. Make sure key starts with "rnd_"
3. Make sure it's not expired (create new if needed)
```

### "Deployment shows error"?
```
1. Check Render dashboard → Logs
2. Common issues:
   - Missing environment variables
   - Port not set to 8000
   - Database URL missing
3. Fix in Render dashboard → Settings → Environment
4. Redeploy with script
```

### Frontend/Backend not responding?
```
Wait 2-3 minutes (deployment in progress)
Then test again:
- Frontend: https://[url].onrender.com
- Backend: https://[url].onrender.com/api/v1/health
```

---

## 📊 QUICK REFERENCE

| Task | Command |
|------|---------|
| Deploy | `.\quick-deploy-render.ps1` |
| Check status | Visit render.com dashboard |
| View logs | Dashboard → Logs tab |
| Redeploy | Run script again |
| Update code | Edit files + script again |

---

## 💡 TIPS

**Fastest path:**
1. Have credentials ready
2. Run `.\quick-deploy-render.ps1`
3. Done! Go live

**Continuous deployment:**
1. Enable auto-deploy in Render
2. `git push origin main` = auto-deploys
3. Zero manual steps

**Environment variables:**
- Backend needs: DATABASE_URL, REDIS_URL, STRIPE keys
- Already configured in Render? They persist!

---

## ✅ YOU'RE READY

Everything is set up for deployment right now.

**Next action:** Run the script with your credentials

```powershell
$env:RENDER_API_KEY = 'your-key'
$env:RENDER_FRONTEND_SERVICE_ID = 'srv-xxxxx'
$env:RENDER_BACKEND_SERVICE_ID = 'srv-xxxxx'
.\quick-deploy-render.ps1
```

**Result:** Live system accepting customers

**Timeline:** 5 minutes from now

Go! 🚀

---

*For detailed reference, see:*
- *RENDER_QUICK_START.md*
- *RENDER_DEPLOYMENT_GUIDE.md*
- *quick-deploy-render.ps1*
