# 🚀 Quick Start: From Zero to Revenue in 30 Minutes

This guide walks you through getting the system live and accepting real payments **today**.

---

## Part 1: Local Testing (5 minutes)

### Step 1: Start the System
```powershell
cd F:\TitanForge
.\STARTUP.ps1
```

Wait for the startup summary. You'll see:
```
📍 URLS:
  • Frontend:     http://localhost:5173
  • Backend API:  http://localhost:8000
  • API Docs:     http://localhost:8000/docs
```

### Step 2: Open and Explore
1. Open http://localhost:5173 in your browser
2. Click "Sign Up" and create a test account
3. Navigate to "Pricing"
4. Click "Subscribe to Basic Plan"

### Step 3: Test Payment Flow
Use these Stripe test cards:
- **Successful payment:** `4242 4242 4242 4242`
- **Declined payment:** `4000 0000 0000 0002`
- **Authentication required:** `4000 0000 0000 3220`

Expiry: Any future date  
CVC: Any 3 digits

**Expected:** Payment processed, subscription created, customer dashboard updated

---

## Part 2: Switch to Real Stripe Keys (5 minutes)

### Step 1: Get Your Keys
1. Go to https://dashboard.stripe.com
2. Sign in (or create free account)
3. Navigate to "Developers" → "API Keys"
4. Copy your **Publishable Key** and **Secret Key**

### Step 2: Update .env File
Edit `F:\TitanForge\.env`:
```bash
STRIPE_API_KEY=sk_live_YOUR_ACTUAL_SECRET_KEY_HERE
STRIPE_WEBHOOK_SECRET=whsec_YOUR_WEBHOOK_SECRET_HERE
```

### Step 3: Restart System
```powershell
# Stop existing system (Ctrl+C)
# Then:
.\STARTUP.ps1
```

**Now you're accepting real payments!**

---

## Part 3: Deploy to Production (15 minutes)

### Option A: Deploy to Render (Recommended for Beginners)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Money machine ready for production"
   git push origin main
   ```

2. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your TitanForge repo

3. **Configure Service**
   - **Runtime:** Docker
   - **Branch:** main
   - **Build command:** Leave empty (Dockerfile used)
   - Add environment variables:
     ```
     DATABASE_URL=postgresql://...render.com/...
     STRIPE_API_KEY=sk_live_YOUR_KEY
     STRIPE_WEBHOOK_SECRET=whsec_YOUR_KEY
     SECRET_KEY=<generate-random-string>
     REDIS_URL=redis://...
     ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait ~5 minutes for deployment
   - You'll get a URL like `https://titanforge-ai.onrender.com`

### Option B: Deploy to Vercel (Frontend Only)

For frontend static deployment:

1. Create `frontend/vercel.json`:
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": "dist",
     "env": {
       "VITE_API_URL": "@vite_api_url"
     }
   }
   ```

2. Push to GitHub and connect Vercel
3. Vercel will auto-deploy on every push

### Option C: Deploy to Railway

1. Go to https://railway.app
2. Click "Start Project"
3. Select "Deploy from GitHub"
4. Connect TitanForge repo
5. Railway auto-detects Dockerfile
6. Add environment variables (same as Render)
7. Deploy!

---

## Part 4: Wire Up Custom Domain (10 minutes)

### If You Have DNS Access to realmstoriches.xyz

1. Go to your DNS provider (currently Wix)
2. Add CNAME record:
   ```
   Name: www
   Type: CNAME
   Value: titanforge-ai.onrender.com  (or your deployment URL)
   ```

3. Wait 5-30 minutes for DNS propagation

4. Update backend `.env`:
   ```
   FRONTEND_URL=https://www.realmstoriches.xyz
   ALLOWED_HOSTS=www.realmstoriches.xyz
   ```

5. Restart system

**Your site is now at:** www.realmstoriches.xyz

### If DNS is Still Locked

Use the auto-generated domain from your host for now:
- Render: `https://titanforge-ai.onrender.com`
- Railway: `https://titanforge-ai-production.up.railway.app`
- Vercel: `https://titanforge-ai.vercel.app`

**Path to recovery:**
1. Contact Wix support to regain DNS access
2. OR transfer domain to new registrar (Namecheap, GoDaddy)
3. Once DNS is yours, redirect to deployment URL
4. Full custom domain in <1 hour

---

## Part 5: Set Up Email (Optional but Recommended)

### For Professional Outreach

**Option 1: Use SendGrid (Free tier)**
1. Sign up at https://sendgrid.com
2. Verify domain
3. Get API key
4. Update `.env`:
   ```
   SENDGRID_API_KEY=SG.your_key_here
   ```

**Option 2: Use Gmail + Mailgun (Free tier)**
1. Get Mailgun domain at https://mailgun.com
2. Use Mailgun for high-volume outreach
3. Use Gmail for personal reply-to

---

## Part 6: First Customer Acquisition (5 minutes)

### Launch Strategy

**Day 1: Test with Friends**
- Share link: `https://www.realmstoriches.xyz` (or your deployment URL)
- Ask 5 trusted people to create accounts
- Offer first month free for feedback

**Day 2-3: Product Hunt**
- Post to https://producthunt.com
- Title: "TitanForge AI - AI Software Development Agency as a Service"
- Offer: "Launch special: 50% off first 3 months"

**Day 4-7: Cold Email**
- Use agent-driven outreach (available in system)
- Or manually email prospects

**Week 2: Community**
- Reddit: r/SaaS, r/startup, r/Entrepreneur
- HackerNews: If product ready
- IndieHackers: Community posting

---

## Revenue Model Recap

### Your 3 Current Income Streams

**Stream 1: SaaS Subscriptions** (Monthly)
- Basic: $2,999/month
- Professional: $4,999/month
- Enterprise: Custom pricing
- **Your Goal:** 10 customers = $35K+/month

**Stream 2: Productized Services** (Per-project)
- "Audit Your Code": $1,500
- "Build 5 API Endpoints": $5,000
- "Architecture Review": $3,000
- **Your Goal:** 5 projects/month = $15K+/month

**Stream 3: Lead Generation** (When Wired)
- Sell leads to other agencies
- $25-$100 per qualified lead
- **Your Goal:** 100 leads/month = $2.5K-$10K/month

**Year 1 Conservative Projection:**
- Month 1-3: $0 (setup)
- Month 4-6: $20K/month (first customers)
- Month 7-12: $50K/month (scaling)
- **Year 1 Total:** ~$300K ARR

**Year 1 Aggressive Projection:**
- Month 1: $5K (beta customers)
- Month 2-3: $25K/month (rapid growth)
- Month 4-12: $80K+/month (scaling)
- **Year 1 Total:** ~$800K ARR

---

## Monitoring Your Revenue

### Check Dashboard
Go to http://localhost:8000/docs → Try out these endpoints:

**See all customers:**
```
GET /admin/users
```

**Check subscriptions:**
```
GET /admin/subscriptions
```

**See revenue:**
```
GET /admin/revenue-report
```

### Real-Time Stripe Dashboard
Monitor all transactions at https://dashboard.stripe.com/transactions

---

## What Happens When a Customer Signs Up

1. **Frontend:** Customer clicks "Subscribe"
2. **Checkout:** Stripe Checkout window opens
3. **Payment:** Customer enters credit card
4. **Backend:** Payment webhook received
5. **Database:** Subscription created in DB
6. **Email:** Confirmation email sent
7. **Dashboard:** Customer can access services
8. **Your Account:** Money appears in Stripe (minus 2.9% + $0.30 fee)

**Total time:** ~30 seconds  
**Your revenue:** Immediate (minus Stripe fees)

---

## Troubleshooting

**"Payment failed"**
- Check Stripe test mode vs live mode
- Verify keys in `.env`
- Restart with `.\STARTUP.ps1`

**"Domain not found"**
- DNS changes take 5-30 minutes
- Check DNS propagation: https://dnschecker.org
- Use deployment URL until DNS updates

**"Can't create account"**
- Check backend logs: http://localhost:8000/docs
- Verify database running: `docker ps`
- Database might need migration

**"No emails being sent"**
- Verify email service API key in `.env`
- Check spam folder
- Test with phone number instead initially

---

## Next Immediate Actions

- [ ] Run `.\STARTUP.ps1` and test locally
- [ ] Sign up on Stripe.com and get live keys
- [ ] Choose deployment platform (Render recommended)
- [ ] Deploy and test payments with real card
- [ ] Share link with 5 people for feedback
- [ ] Post on Product Hunt / Reddit / IndieHackers
- [ ] Set up cold email outreach
- [ ] Track first paying customer

---

## The Reality Check

You now have:
✅ A fully functional, money-accepting system  
✅ Professional infrastructure  
✅ Three revenue streams  
✅ Everything you need to sell  

What you still need:
⏳ Customers (your sales/marketing job)  
⏳ Continuous optimization (based on feedback)  
⏳ Content & marketing (next sprint)  
⏳ Sales automation (available but requires setup)  

**The machine works. Now go sell it. 💰**

---

## Support & Questions

- **Technical:** Check http://localhost:8000/docs
- **Payments:** See Stripe docs at https://stripe.com/docs
- **Deployment:** See specific platform (Render/Railway/Vercel) docs
- **Email:** Check SendGrid/Mailgun docs

**You've got this. Go make money. 🚀**
