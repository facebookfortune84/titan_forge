# 🚀 TitanForge Manual Startup Guide

If the automated startup script doesn't work in your environment, follow these manual steps.

---

## Prerequisites

Ensure you have installed:
- Docker Desktop (https://docker.com/products/docker-desktop)
- Node.js 18+ (https://nodejs.org)
- Python 3.9+ (https://python.org)
- Git (https://git-scm.com)

---

## Step 1: Start Docker Services (5 minutes)

### On Windows (PowerShell):

```powershell
cd F:\TitanForge
docker-compose up -d db redis
```

This starts PostgreSQL and Redis in background containers.

**Verify they're running:**
```powershell
docker ps
# Should see: titanforge_db and titanforge_redis running
```

---

## Step 2: Install Backend Dependencies (3 minutes)

### On Windows (PowerShell):

```powershell
cd F:\TitanForge\titanforge_backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Step 3: Start Backend (Leave Running)

### In a PowerShell terminal (keep open):

```powershell
cd F:\TitanForge\titanforge_backend
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH = "."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

✅ Backend is running at: http://localhost:8000

---

## Step 4: Install Frontend Dependencies (2 minutes)

### In a NEW PowerShell terminal:

```powershell
cd F:\TitanForge\frontend
npm install
```

---

## Step 5: Start Frontend (Leave Running)

### In another NEW PowerShell terminal:

```powershell
cd F:\TitanForge\frontend
npm run dev
```

**Expected output:**
```
  VITE v7.3.1  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

✅ Frontend is running at: http://localhost:5173

---

## Step 6: Verify Everything Works

### Open in Browser:
- **Frontend:** http://localhost:5173
- **Backend Docs:** http://localhost:8000/docs

### Create a Test Account:
1. Go to http://localhost:5173
2. Click "Sign Up"
3. Enter email and password
4. Click "Create Account"

### Test Payment Flow:
1. Go to "Pricing"
2. Click "Subscribe to Basic Plan"
3. Use Stripe test card: `4242 4242 4242 4242`
4. Expiry: Any future date
5. CVC: Any 3 digits
6. Click "Pay"

**Expected:** Payment succeeds, account upgraded

---

## Troubleshooting

### Docker won't start
```bash
# Make sure Docker Desktop is running (check system tray)
# On Mac/Linux: docker ps should show containers
```

### Backend fails to start
```bash
# Check port 8000 isn't in use:
netstat -ano | findstr :8000
# If in use, kill: taskkill /PID <PID> /F

# Check PYTHONPATH:
$env:PYTHONPATH = "."
```

### Frontend won't compile
```bash
# Clear cache and rebuild:
cd frontend
rm -r node_modules
npm install
npm run dev
```

### Database connection fails
```bash
# Check Docker containers:
docker ps

# Check database logs:
docker logs titanforge_db
```

---

## Stopping Services

### To stop everything:

1. **Frontend terminal:** Press `Ctrl+C`
2. **Backend terminal:** Press `Ctrl+C`
3. **Stop Docker services:**
   ```powershell
   docker-compose down
   ```

---

## Running on a Different Machine

If deploying to production, see:
- [QUICK_START_MONETIZATION.md](QUICK_START_MONETIZATION.md) - Full production guide
- [PRODUCTION_READY_VERIFICATION.md](PRODUCTION_READY_VERIFICATION.md) - Verification checklist

---

## Questions?

Check the documentation:
- API Docs: http://localhost:8000/docs
- README: See project README.md
- Monetization: See QUICK_START_MONETIZATION.md
- Status: See MONEY_MACHINE_STATUS.md

---

## Next: Deploy to Production

Once verified locally, see [QUICK_START_MONETIZATION.md](QUICK_START_MONETIZATION.md) for deployment to:
- Render.com
- Railway
- Vercel
- Custom VPS
- AWS/GCP/Azure

💰 Ready to make money!
