"""Quick startup and testing instructions for TitanForge Sales System."""

# ============================================================
# 5-MINUTE STARTUP & TESTING GUIDE
# ============================================================

"""
STEP 1: START THE SYSTEM (1 minute)
═══════════════════════════════════

cd F:\TitanForge
docker-compose up -d

Wait 15 seconds for services to start, then verify:
docker-compose ps

Should show:
  ✅ titanforge_backend (port 8000)
  ✅ titanforge_db (port 5432)
  ✅ titanforge_redis (port 6379)

If any show "unhealthy", wait 10 more seconds and check again.


STEP 2: TEST THE PRICING TIERS (30 seconds)
═════════════════════════════════════════════

Open browser or use curl:

Test Basic Tier:
  curl http://localhost:8000/api/v1/pricing/basic

Test Pro Tier:
  curl http://localhost:8000/api/v1/pricing/pro

Should return:
  {
    "tier": "basic",
    "monthly_cents": 299900,  ($2,999)
    "yearly_cents": 249900,   ($2,499/month annual)
    ...
  }

✅ If you see the JSON = PRICING IS LIVE


STEP 3: TEST LEAD CAPTURE (1 minute)
════════════════════════════════════

Create a test lead:
  curl -X POST http://localhost:8000/api/v1/leads \
    -H "Content-Type: application/json" \
    -d '{"email":"testuser@example.com"}'

Response should include:
  "id": "[UUID]"
  "status": "new"
  "created_at": "[timestamp]"

List all leads:
  curl http://localhost:8000/api/v1/leads

✅ If you see the lead listed = LEAD CAPTURE IS WORKING


STEP 4: TEST SALES FUNNEL TRACKING (1 minute)
══════════════════════════════════════════════

Track an impression:
  curl "http://localhost:8000/api/v1/sales/track/impression?utm_source=google&utm_campaign=launch"

Download lead magnet:
  curl -X POST http://localhost:8000/api/v1/sales/lead-magnet/download \
    -H "Content-Type: application/json" \
    -d '{
      "email":"customer@company.com",
      "company_name":"Acme Corp",
      "company_size":"51-500",
      "utm_source":"linkedin"
    }'

Get sales pipeline:
  curl http://localhost:8000/api/v1/sales/funnel/pipeline

Get dashboard:
  curl http://localhost:8000/api/v1/sales/funnel/dashboard

✅ If you see pipeline data = FUNNEL IS LIVE


STEP 5: VERIFY AUTHENTICATION (30 seconds)
═════════════════════════════════════════════

Register a user:
  curl -X POST http://localhost:8000/api/v1/auth/register \
    -H "Content-Type: application/json" \
    -d '{
      "email":"user@demo.com",
      "password":"SecurePass123!",
      "full_name":"Test User"
    }'

Login:
  curl -X POST http://localhost:8000/api/v1/auth/login \
    -d "username=user@demo.com&password=SecurePass123!"

You should get a JWT token response.

✅ If you get a token = AUTH IS WORKING


════════════════════════════════════════════════════════════
TEST SUMMARY
════════════════════════════════════════════════════════════

If all 5 steps show ✅:

  ✅ System is running
  ✅ Pricing is deployed
  ✅ Lead capture is live
  ✅ Sales funnel is tracking
  ✅ Authentication is working
  
  => YOU ARE READY FOR CUSTOMER ACQUISITION


════════════════════════════════════════════════════════════
TO STOP THE SYSTEM
════════════════════════════════════════════════════════════

docker-compose down

(Data persists in volumes - won't be deleted)


════════════════════════════════════════════════════════════
TO RESET EVERYTHING (Clean slate)
════════════════════════════════════════════════════════════

docker-compose down -v

(Deletes all data - use only for testing)


════════════════════════════════════════════════════════════
QUICK VERIFICATION (60 seconds)
════════════════════════════════════════════════════════════

Copy this script and run it:

#!/bin/bash

echo "Testing TitanForge Sales System..."

# Test pricing
echo "[1/5] Testing pricing..."
curl -s http://localhost:8000/api/v1/pricing/basic | grep "299900" && echo "  ✅ Pricing OK" || echo "  ❌ Failed"

# Test leads
echo "[2/5] Testing leads..."
curl -s http://localhost:8000/api/v1/leads | grep "id" && echo "  ✅ Leads OK" || echo "  ❌ Failed"

# Test agents
echo "[3/5] Testing agents..."
curl -s http://localhost:8000/api/v1/agents | grep "agents" && echo "  ✅ Agents OK" || echo "  ❌ Failed"

# Test sales funnel
echo "[4/5] Testing funnel..."
curl -s http://localhost:8000/api/v1/sales/funnel/pipeline | grep "customers" && echo "  ✅ Funnel OK" || echo "  ❌ Failed"

# Test dashboard
echo "[5/5] Testing dashboard..."
curl -s http://localhost:8000/api/v1/sales/funnel/dashboard | grep "customers" && echo "  ✅ Dashboard OK" || echo "  ❌ Failed"

echo ""
echo "All tests complete!"


════════════════════════════════════════════════════════════
TRAFFIC GENERATION QUICK START
════════════════════════════════════════════════════════════

Your lead magnet is now live at:
  GET http://localhost:8000/api/v1/sales/lead-magnet/download

Preview available:
  GET http://localhost:8000/api/v1/sales/lead-magnet/preview

Funnel tracking is active - every visitor/lead is tracked through:
  1. Impression → 2. Download → 3. Demo → 4. Trial → 5. Customer

Real-time metrics dashboard:
  GET http://localhost:8000/api/v1/sales/funnel/dashboard


════════════════════════════════════════════════════════════
NEXT STEPS: GO GET CUSTOMERS
════════════════════════════════════════════════════════════

1. All systems verified ✅
2. Pricing deployed ✅
3. Lead magnet live ✅
4. Sales funnel tracking ✅
5. Customer acquisition system ready ✅

Share this link with sales team:
  http://localhost:8000/api/v1/sales/funnel/dashboard

For each customer acquired:
  POST http://localhost:8000/api/v1/sales/customer/created
    email, tier, amount

Track revenue in real-time on the dashboard.
"""
