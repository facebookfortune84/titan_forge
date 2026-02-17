# 🚀 FREE DEPLOYMENT: Vercel + Railway

**Status:** ✅ Ready for immediate free deployment  
**Cost:** $0 (both have free tiers)  
**Time:** ~5 minutes total  

---

## 🎯 YOUR FREE OPTIONS

### Option A: Ultra-Simple (Just Vercel)
```
Perfect for: Testing today
Cost: Free forever
What you get: Frontend only (landing page + signup)
Missing: Backend API + payments (but can test)

# You're already signed in as: realmstoriches
vercel deploy --prod
```

**Frontend URL:** `https://titanforge-frontend.vercel.app`

---

### Option B: Complete Free System ✅ RECOMMENDED
```
Perfect for: Full launch with backend
Cost: Free ($5/month credit on Railway = way more than you need)
What you get: Frontend + Backend + Database + Everything

Step 1: Deploy frontend to Vercel
Step 2: Deploy backend to Railway
Step 3: Connect them
Step 4: LIVE!
```

---

## 🚀 OPTION B: COMPLETE FREE DEPLOYMENT

### Step 1: Deploy Frontend to Vercel (1 minute)

You're already signed in. Just run:

```powershell
cd frontend
vercel deploy --prod
```

**Result:** Frontend live at `https://titanforge-frontend.vercel.app`

---

### Step 2: Deploy Backend to Railway (3 minutes)

#### 2A. Install Railway CLI
```bash
npm install -g @railway/cli
```

#### 2B. Login to Railway
```bash
railway login
```
- Opens browser
- Click "Continue with GitHub"
- Authorize
- Done

#### 2C. Deploy Backend

```bash
# From project root
railway up
```

**First time:** Railway will ask to create a project. Click "Create a new project".

**Result:** Backend live at `https://your-project.up.railway.app`

---

### Step 3: Connect Frontend to Backend (30 seconds)

The frontend needs to know where the backend is.

#### Edit `frontend/.env.production`:

```
VITE_API_URL=https://your-railway-backend.up.railway.app
VITE_STRIPE_PUBLIC_KEY=pk_test_xxxxx
```

#### Get your Railway backend URL:
1. Go to railway.app/dashboard
2. Click your project
3. Click the backend service
4. Copy the "Public URL"

#### Redeploy frontend:
```powershell
cd frontend
vercel deploy --prod
```

---

## 📊 WHAT YOU GET (FREE)

### Vercel Frontend
✅ Unlimited deployments  
✅ Automatic SSL/HTTPS  
✅ CDN (fast everywhere)  
✅ Custom domain support  
✅ $0 forever (free tier)  

### Railway Backend
✅ PostgreSQL database included  
✅ Redis cache included  
✅ $5/month free credit  
✅ Auto-scaling (you won't need it on free tier)  
✅ Enough for 100s of users  

---

## ⏱️ TOTAL TIME: 5 MINUTES

| Task | Time |
|------|------|
| Deploy frontend | 1 min |
| Deploy backend | 2 min |
| Connect them | 1 min |
| Test | 1 min |
| **Total** | **5 min** |

---

## 🧪 VERIFY IT WORKS

### Test 1: Frontend loads
```
Visit: https://titanforge-frontend.vercel.app
Should see: Landing page with "Ship Code 3x Faster"
```

### Test 2: Backend responds
```bash
curl https://your-railway-backend.up.railway.app/api/v1/health
# Should return: {"status": "healthy"}
```

### Test 3: Signup works
```
1. Click "Get 14 Days Free" on landing page
2. Fill form + submit
3. Should see success page
4. Check Railway logs for API calls
```

### Test 4: Payment flow (test mode)
```
1. Complete signup
2. Go to pricing page
3. Click "Get 14 Days Free" again → upgrade option
4. Card: 4242 4242 4242 4242
5. Should process (test mode)
6. Check Stripe dashboard for transaction
```

---

## 📋 QUICK CHECKLIST

### Before you start:
- [ ] You're in F:\TitanForge directory
- [ ] Node.js installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Vercel CLI installed (`vercel --version`)
- [ ] GitHub account (for Railway login)

### Deployment steps:
- [ ] `vercel deploy --prod` (frontend)
- [ ] `npm install -g @railway/cli`
- [ ] `railway login`
- [ ] `railway up` (backend)
- [ ] Edit `.env.production` with Railway URL
- [ ] `vercel deploy --prod` (update frontend)
- [ ] Test in browser

### After deployment:
- [ ] Frontend URL bookmarked
- [ ] Backend URL copied
- [ ] Environment variables updated
- [ ] All tests passing
- [ ] Ready for marketing

---

## 🆘 TROUBLESHOOTING

### "vercel command not found"
```bash
npm install -g vercel
```

### "railway command not found"
```bash
npm install -g @railway/cli
```

### "Frontend won't load"
```
Check:
1. URL is correct (https://titanforge-frontend.vercel.app)
2. Not a typo in Vercel deploy output
3. Vercel dashboard shows it deployed successfully
```

### "Backend not responding"
```
Check:
1. Railway deployment complete (dashboard shows "Running")
2. Public URL is correct
3. Try curl: https://url.up.railway.app/api/v1/health
4. Check Railway logs for errors
```

### "Signup form fails"
```
Check:
1. VITE_API_URL in .env.production is correct
2. Frontend rebuilt after changing .env
3. Backend is responding (health check passes)
4. No CORS errors in browser console (F12)
```

### "Payment test fails"
```
Check:
1. Stripe API keys are correct
2. Using test cards (4242 4242 4242 4242)
3. Check Stripe dashboard → Logs for errors
```

---

## 💰 COST BREAKDOWN

| Service | Free Tier | Your Usage |
|---------|-----------|-----------|
| Vercel | ✅ Unlimited | Frontend |
| Railway | ✅ $5/month credit | Backend + DB |
| Total | **$0/month** | Everything |

Railway's $5 credit is more than enough for your first 1000 customers!

---

## 🎯 YOUR NEXT STEP

### Choose your deployment:

**Option A: Fast (Vercel only, 1 min)**
```powershell
cd frontend
vercel deploy --prod
```

**Option B: Complete (Vercel + Railway, 5 min)**
```powershell
# See steps above
```

Pick one and execute! ⚡

---

## 📚 REFERENCE

- Vercel docs: https://vercel.com/docs
- Railway docs: https://railway.app/docs
- GitHub login: https://github.com/login

---

**Ready?** Let's deploy! 🚀
