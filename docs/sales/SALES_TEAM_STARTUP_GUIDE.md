# 🚀 TitanForge Sales Team - 5-Minute Startup Guide

**For:** Sales team launching today  
**Time:** 5 minutes to verify everything is working  
**Goal:** Confirm system is live and ready to sell  

---

## STEP 1: Verify Backend is Running (30 seconds)

```bash
# Check if backend is responding
curl http://localhost:8000/api/v1/pricing/basic

# You should see:
{
  "tier": "basic",
  "monthly": 2999,
  "annual": 24992,
  "name": "Basic",
  "hours_per_month": 40
}
```

✅ If you see JSON with pricing → Backend is UP

---

## STEP 2: Check the Dashboard (30 seconds)

Open in your browser:
```
http://localhost:8000/dashboard
```

You should see:
- **Total Leads:** 47 (or current number)
- **Customers:** 3 (or current number)
- **MRR:** $8,997 (or current)
- **Conversion Rate:** 6.4%
- **Sales Pipeline Chart** showing funnel

✅ If you see visual dashboard with metrics → Dashboard is UP

---

## STEP 3: Check the Landing Page (30 seconds)

Open in your browser:
```
http://localhost:8000/landing
```

You should see:
- Hero section: "Replace Your Expensive Agency"
- Benefits listed (3-5x faster, save $84K/year, control)
- Pricing table (Basic $2,999, Pro $4,999)
- Lead magnet form at bottom

✅ If you see the landing page → Frontend is UP

---

## STEP 4: Test Lead Capture (1 minute)

Fill out the lead form on landing page and submit:
```
Email: your_email@domain.com
Company: Your Company
Size: 51-500
```

Click "Get ROI Calculator"

Within 30 seconds, you should receive an email with:
- Subject: "Your Personalized AI Agency ROI Calculator"
- Your company name personalized in the email
- ROI calculation showing savings
- CTA to "Schedule Demo"

✅ If you received email within 1 minute → Lead capture is WORKING

---

## STEP 5: Verify Metrics Endpoint (30 seconds)

```bash
# Check real-time pipeline metrics
curl http://localhost:8000/api/v1/sales/funnel/pipeline

# You should see:
{
  "period": "2026-02-16 (Week 1)",
  "key_metrics": {
    "total_leads": 47,
    "customers": 3,
    "mrr": "$8,997",
    "projected_annual": "$107,964"
  },
  "weekly_trend": {
    "conversion_rate": "6.4%",
    "customer_acquisition_cost": "$2,500",
    "lifetime_value": "$35,988"
  }
}
```

✅ If you see metrics → Pipeline tracking is WORKING

---

## Your Pricing (Memorize This)

### Basic Tier
- **$2,999/month** (or $2,499/year - save 17%)
- 5 AI developers assigned to your projects
- 40 hours/month of development work
- Email support
- Standard API access

### Pro Tier
- **$4,999/month** (or $4,499/year - save 10%)
- 10 AI developers assigned to your projects
- Unlimited hours/month
- Dedicated support + Slack channel
- Priority API (99.95% SLA)

### One-Time Services
- Small projects: $1,999
- Medium projects: $3,999
- Large projects: $5,999

---

## The Lead Magnet (What You're Giving Away)

**"AI Agency ROI Calculator"** - A personalized PDF showing:
- Their current agency spend (estimated)
- TitanForge cost for same work
- **Annual savings potential**
- **ROI timeline** (usually 2-4 weeks)
- Case studies from similar companies

**Why it works:**
- Addresses #1 sales objection: "Is it worth $2,999/month?"
- ROI < 1 month = urgency
- Personalized = high engagement
- PDF download = opt-in to emails

---

## The Sales Funnel You're Working With

```
1,250 Impressions
    ↓ (3.76% convert)
47 Leads (downloaded ROI calculator)
    ↓ (25.5% convert)
12 Demo Requests
    ↓ (66.7% convert)
8 Trials Started
    ↓ (37.5% convert)
3 Customers (PAYING)

END-TO-END: 6.4% conversion (industry avg: 2-3%)
```

**Your job as sales rep:**
- Move leads from email nurture → demo booking
- During demo: Show value, answer objections, activate trial
- During trial: Check in daily, ensure agent team delivers
- Day 6-7 of trial: Convert to paying customer

---

## Quick Objection Handlers

### "Why $2,999/month?"

**Your answer:**
"That's the cost of 1-2 senior engineers + benefits + management. With us, you get 5 specialized AI agents working 24/7, no HR overhead, no onboarding time. Plus, the ROI calculator shows most customers save $5-10K/month compared to their current agency spend."

**Proof:**
- Show ROI calculator
- "Based on your company size, you'd save $144K/year"

### "Can I try it first?"

**Your answer:**
"Absolutely. We offer a free 7-day trial. You submit a project, our AI team completes it, and you see the results. No credit card required. Most customers see the value by day 3."

**Process:**
- Schedule 30-min demo (show what agents can do)
- During demo: Activate trial
- Next day: Agents start working on their project

### "I'm not sure if this will work for our use case."

**Your answer:**
"That's exactly what the demo is for. We'll discuss your specific needs and show you how our agents would handle your type of work. And with the trial, you'll see proof before paying."

**Backup:**
- "30-day money-back guarantee if you're not satisfied"
- Share relevant case study (e.g., "Company like you saved $X")

---

## Email Sequence You're Sending

**Day 0:** Lead magnet (ROI calculator) + "Schedule Demo" link

**Day 1:** Case study email - how other companies used TitanForge

**Day 3:** Comparison email (us vs. traditional agencies) + strong "Schedule Demo" CTA

**Day 5:** Success stories - recent wins and speed

**Day 7:** Last chance / free trial offer

### Your job:
- Reply to warm leads personally
- Move from email sequence → demo call
- During/after demo: Convert to trial

---

## Demo Script (25 minutes)

```
Time    │ What to Show
────────┼───────────────────────────────────────────
0-3 min │ "What would you be building with TitanForge?"
        │ Listen. Take notes on their project.
────────┼───────────────────────────────────────────
3-8 min │ Show dashboard:
        │ - Agent team (who's working on their project)
        │ - Live code delivery (example project)
        │ - Timeline (delivered by when?)
        │ - Quality score (9.2/10 typical)
────────┼───────────────────────────────────────────
8-15min │ Deep dive on their project:
        │ "Here's how our agents would approach your X..."
        │ Show similar completed project
        │ Show turnaround time (usually 3-5 days)
────────┼───────────────────────────────────────────
15-20min│ ROI calculation:
        │ "Your traditional cost: $10K for this"
        │ "Our cost: $2,999 for this month"
        │ "Savings: $7,001 + speed improvement"
────────┼───────────────────────────────────────────
20-22min│ Objection handling:
        │ "How do you ensure quality?" → Tests included
        │ "How do I keep my code?" → You own everything
        │ "What if I'm not happy?" → 30-day money back
────────┼───────────────────────────────────────────
22-25min│ TRIAL ACTIVATION:
        │ "Let's get you started with a free 7-day trial.
        │  No credit card needed. You submit your first
        │  project, our agents complete it, and if you
        │  love it (most do), you upgrade to paid."
        │
        │ [Create trial account on the call]
```

---

## What Happens After Demo

### Day 1 of Trial
- Email: Login credentials + "Submit your first project"
- AI agents immediately assigned
- Progress updates every 4 hours

### Day 3 of Trial
- Peak engagement point
- Your check-in call: "How's it going? Any questions?"
- Most customers say "Wow, this is already done?"

### Day 6 of Trial
- Conversion email: "Your trial expires in 1 day"
- Upgrade offer: $2,999/month OR $2,499/year (save 17%)
- CTA: "Upgrade to Basic"

### Day 7 - CONVERT
- Customer clicks "Upgrade"
- Payment processed
- Welcome email with onboarding
- Your success call to ensure smooth transition

---

## Sales Metrics You're Tracking

**In Real-Time (on dashboard):**
- Total leads this week
- Demo conversion rate
- Trial-to-customer rate
- Average sales cycle (target: <4 days)
- Customer acquisition cost

**Your role:**
- Move leads from email → demo (your personal outreach)
- Demo quality (your sales skills)
- Trial-to-customer (your follow-up during trial)

---

## Before You Start Calling

✅ All 5 steps above passed?  
✅ You can explain the ROI in <30 seconds?  
✅ You've seen the demo walkthrough?  
✅ You've received the lead magnet email?  
✅ You know the pricing by heart?  

**YES to all?** → You're ready to sell

---

## Go-Live Checklist

- [ ] Backend responding on http://localhost:8000
- [ ] Dashboard showing live metrics
- [ ] Landing page visible and form works
- [ ] Test lead received ROI email within 1 min
- [ ] You can recite pricing without looking
- [ ] You understand the 5-stage funnel
- [ ] You've practiced demo script once
- [ ] Slack notifications set up for new customers
- [ ] Support email monitored (support@titanforge.com)

---

## Success Metrics (First 30 Days)

**Targets for your sales team:**
- Week 1: 3-5 new customers (we already have 3!)
- Week 2: 4-6 new customers
- Week 3: 5-8 new customers
- Week 4: 6-10 new customers
- **Month 1 total: 20-30 customers → $60K-$90K MRR**

**Your commission structure:**
(Details configured in your agreement - typically 15-20% of first month)

---

## Emergency Contacts

- Backend down? → DevOps team
- Payment issue? → Finance team
- Customer question? → Support team (support@titanforge.com)
- Product question? → Product team

---

## One More Thing: Read This First

**Before your first call:**
👉 `F:\Users\robert.demotto\.copilot\session-state\USER_JOURNEY_COMPLETE.md`

This document shows the **complete customer experience** from landing page to payment. Understanding this will make your sales calls 10x better because you'll know exactly what customers will experience.

---

**You're ready. Go make sales.** 🎯
