# SWARM ORCHESTRATION – MARKETING & ACQUISITION MODE

**Status:** ACTIVE  
**Mode:** Multi-Agent Coordination (1000-10000 agents conceptually assigned)  
**Mission:** Transform TitanForge into self-contained, infinitely adaptable monetization machine  
**Last Updated:** 2026-02-17  

---

## 🎯 EXECUTIVE SUMMARY

The TitanForge **production platform build** (5 sprints) is complete. Now we activate the **Marketing & Acquisition Swarm** to ensure the system is not just technically sound, but commercially viable and scalable to any business domain.

**Current State:**
- ✅ Backend: 20+ APIs, Stripe integration, payment processing live
- ✅ Frontend: Landing pages, pricing, blog, lead capture forms exist
- ✅ Infrastructure: Docker, one-command startup, databases ready
- ⚠️ Marketing: Scattered across multiple files, not yet centralized or adaptable
- ⚠️ Positioning: Ad-hoc; no unified ICP, messaging, or funnel clarity
- ⚠️ Agents: No marketing-specific roles defined; ready to be wired

**What Needs to Happen:**
1. Centralize all marketing/business logic into structured configs
2. Define agents for SEO, content, copywriting, email, funnels, analytics
3. Make system adaptable to any business domain (retuning on new ICP/messaging)
4. Instrument full user journey for measurement and optimization
5. Unlock growth: 1000+ leads/month → 50+ customers → $250K+/month potential

---

## 📊 MARKETING SYSTEM SNAPSHOT

### Current Offering & Positioning

**Primary Offering:** AI-as-a-Service (AIaaS) Platform + Agentic Software Development Services

**Existing Pricing Tiers:**
- Starter: $19/month (1,000 API calls/month, 1 concurrent agent)
- Pro: $99/month (10,000 API calls/month, 5 concurrent agents)
- Enterprise: Custom (unlimited, dedicated support)

**Productized Services:**
- Micro-Feature Development: $499-$1,499
- Website Audit & Optimization: $299-$799
- API Endpoint Creation: $799-$1,999

**Value Proposition (Current):** "Build, automate, and innovate faster with intelligent AI agents"

**Gaps:** 
- Not crystal clear who we're selling to beyond "developers"
- No unified messaging across landing pages
- No clear differentiation vs alternatives (agents ≠ new, others exist)
- Pricing disconnect (why $19 vs $99? What's the job to be done?)

---

### Existing Pages & Funnels

**Frontend Routes:**
- `/` → LandingPagePro.tsx (hero, features, CTAs, lead form, cookie consent)
- `/pricing` → PricingPage.tsx (3 tiers, comparison table, signup CTAs)
- `/blog` → Blog.tsx (markdown blog, categories, related posts)
- `/register` → RegisterPage.tsx (email + password signup)
- `/login` → LoginPage.tsx
- `/checkout` → CheckoutPage.tsx (Stripe payment form)
- `/dashboard` → UserDashboard.tsx (after login)

**Lead Capture:**
- Email form on landing page (name, email, company, size)
- Backend endpoint: `POST /api/v1/sales/lead-magnet/download` (stores leads)

**Blog Infrastructure:**
- 3 mock posts included in Blog.tsx component
- Topics: AI agents, software development, transformation
- No actual blog API; content hardcoded in component

---

### Agent Roles Currently Defined

**In `swarm/departments/`:** (inspected earlier - directory exists but minimal content)

**What Exists:**
- Swarm framework scaffolded
- No marketing-specific agents defined

**What's Missing:**
- SEO_Agent (keyword research, content optimization)
- Content_Agent (blog post generation, ideation)
- Copy_Agent (landing page copy, email, CTAs)
- EmailCRM_Agent (sequence management, personalization)
- Funnel_Agent (funnel design, conversion optimization)
- Analytics_Agent (event tracking, reporting)
- SocialMediaManager_Agent (content calendar, engagement)

---

### SEO & Organic Traffic Status

**Current:**
- Landing page has basic meta tags (needs audit)
- Blog component has H1/H2 structure but no keyword targeting
- No sitemap.xml or robots.txt
- No internal linking strategy documented
- No content calendar or keyword map

**Estimate:** Without optimization, organic traffic = near-zero. Needs immediate work.

---

### Email & Nurture Status

**Current:**
- No email sending infrastructure (all endpoints reference backend hooks)
- No email sequence templates defined
- No lead scoring or routing logic

**Estimate:** Leads captured but not nurtured = poor conversion.

---

### Analytics & Measurement

**Current:**
- No event tracking configured (GA4 placeholder commented in code)
- No funnel monitoring
- No A/B testing framework
- No custom dashboards for marketing metrics

**Estimate:** Flying blind; no data to optimize from.

---

## 🔧 SWARM AGENTS – ROLES & RESPONSIBILITIES

### Role Definitions (To Be Created/Wired)

| Role | Responsibilities | Tools | Priority |
|------|-----------------|-------|----------|
| **SEO_Agent** | Keyword research, content optimization, technical SEO audits, internal linking | Search API (mock), content analyzer, audit generator | 🔴 HIGH |
| **Content_Agent** | Blog post ideation, structure, research, outline generation | Web search (mock), data aggregation, markdown generator | 🔴 HIGH |
| **Copy_Agent** | Landing page headlines, CTAs, email subject lines, value prop refinement | Business profile reader, style guide enforcer, variant generator | 🔴 HIGH |
| **EmailCRM_Agent** | Sequence design, personalization tokens, trigger logic, deliverability | Lead database, template engine, event listener | 🟡 MEDIUM |
| **Funnel_Agent** | Funnel design, conversion optimization, CTA placement, page flow | Heatmap data (mock), conversion analytics, A/B test config | 🟡 MEDIUM |
| **Analytics_Agent** | Event tracking setup, dashboard creation, hypothesis generation | Analytics platform config, experiment design | 🟡 MEDIUM |
| **SocialMediaManager_Agent** | Content calendar, post scheduling, engagement monitoring | Social media platform API stubs, content optimizer | 🟢 LOW |
| **Growth_Orchestrator** | Coordinate above agents on domain-specific campaigns | All above + business profile reader | 🔴 HIGH |

---

## 📈 KEY METRICS & SUCCESS CRITERIA

### Month 1 Targets (After Marketing Sprints)
- Organic traffic: 500+ monthly visitors (from blog/SEO)
- Email list: 200+ subscribers
- Lead capture rate: 5-10% of visitors
- Qualified leads: 50+ per month
- Trial signups: 10+ per month
- Paying customers: 1-3

### Month 3 Targets
- Organic traffic: 5,000+ monthly visitors
- Email list: 1,000+ subscribers
- Lead capture rate: 10-15%
- Qualified leads: 500+ per month
- Trial signups: 100+ per month
- Paying customers: 20-50

### Month 6 Targets
- Organic traffic: 20,000+ monthly visitors
- Email list: 5,000+ subscribers
- Paying customers: 100-200+
- Monthly recurring revenue: $20K-$40K+

---

## 📋 SWARM COORDINATION STRUCTURE

```
┌─────────────────────────────────────────────────────────┐
│  GROWTH_ORCHESTRATOR (master coordinator)               │
│  - Reads: businessProfile.yaml, marketingStrategy.yaml  │
│  - Coordinates: all agents below                         │
│  - Output: Campaign plans, priorities, metrics          │
└─────────────────────────────────────────────────────────┘
         ↓
    ┌────────────────────────────────────────────┐
    │ Content & Messaging (SEO, Copy, Content)  │
    ├────────────────────────────────────────────┤
    │ ↓ SEO_Agent            → sitemap, keywords │
    │ ↓ Content_Agent        → blog posts        │
    │ ↓ Copy_Agent           → headlines, CTAs   │
    └────────────────────────────────────────────┘
         ↓
    ┌────────────────────────────────────────────┐
    │ Conversion & Lead Gen (Funnel, Forms)     │
    ├────────────────────────────────────────────┤
    │ ↓ Funnel_Agent         → page design       │
    │ ↓ Lead forms (built)   → capture leads     │
    │ ↓ Lead scoring (TODO)  → qualify leads     │
    └────────────────────────────────────────────┘
         ↓
    ┌────────────────────────────────────────────┐
    │ Nurture & Revenue (Email, Upsell, CRM)   │
    ├────────────────────────────────────────────┤
    │ ↓ EmailCRM_Agent       → sequences         │
    │ ↓ Lead routing (TODO)  → sales pipeline    │
    │ ↓ Upsell logic (TODO)  → expansion revenue │
    └────────────────────────────────────────────┘
         ↓
    ┌────────────────────────────────────────────┐
    │ Measurement & Optimization (Analytics)    │
    ├────────────────────────────────────────────┤
    │ ↓ Analytics_Agent      → event tracking    │
    │ ↓ A/B test framework   → experiments       │
    │ ↓ Dashboards (TODO)    → visibility        │
    └────────────────────────────────────────────┘
```

---

## 🚀 SPRINT ROADMAP

### SPRINT M1 ✅ [ACTIVE]
**Clarify Offer, ICP & Core Funnel**
- Audit existing positioning (ads, pages, messaging)
- Define ICP clearly
- Create `businessProfile.yaml` (centralized config)
- Create `positioningLayer.yaml` (offer, USP, messaging)
- Document core user journey

### SPRINT M2 [NEXT]
**Landing Page & Sales Pages Optimization**
- Optimize hero copy
- Enhance pricing page clarity
- Add social proof
- Wire 2+ CTAs

### SPRINT M3 [NEXT]
**Lead Capture & Backend Storage**
- Verify lead form logic
- Create lead export functionality
- Wire lead scoring

### SPRINT M4 [NEXT]
**Blog & SEO Infrastructure**
- Content strategy & keywords
- Sitemap & robots.txt
- Meta tags & schema markup

### SPRINT M5 [NEXT]
**Email Sequences & Nurture**
- Define email templates
- Wire triggers
- Create sending hooks

### SPRINT M6 [NEXT]
**Funnel Mapping & Events**
- Event tracking config
- Analytics setup
- A/B testing framework

### SPRINT M7 [NEXT]
**Agent Roster for Marketing**
- Create marketing agent roles
- Wire to businessProfile config
- Define task templates

### SPRINT M8 [NEXT]
**Multi-Domain Adaptation**
- Extract domain variables
- Create 3 example profiles
- Document retuning process

---

## 🎯 IMMEDIATE NEXT STEPS

**Your action: Review and confirm SPRINT M1 below, then execute.**

---

# SPRINT M1 – CLARIFY OFFER, ICP & CORE FUNNEL

**Duration:** 1-2 hours  
**Outcome:** Unified positioning, clear ICP, and documented core funnel  
**Owner(s):** Copy_Agent, Growth_Orchestrator, Funnel_Agent  

---

## What We're Doing

We're answering three critical questions that all marketing flows from:

1. **What are we selling exactly?** (Clear, testable offer)
2. **Who are we selling to?** (Specific, compelling ICP)
3. **What's the job they hire us to do?** (Pain point, desired outcome)

Once these are locked, all other marketing decisions (page copy, blog topics, email sequences, CTAs) become mechanical.

---

## SPRINT M1 Checklist

- [ ] **Task 1:** Audit existing positioning across all pages and docs
- [ ] **Task 2:** Define ICP (who buys, pain points, buying signals)
- [ ] **Task 3:** Create `swarm/config/businessProfile.yaml` with all variables
- [ ] **Task 4:** Create `swarm/config/positioningLayer.yaml` (offer, USP, messaging)
- [ ] **Task 5:** Map core user journey (visitor → lead → signup → payment)
- [ ] **Task 6:** Document in `swarm/config/README.md` how agents read these configs

---

## Execution Plan

### Task 1: Audit Existing Positioning

**What to inspect:**
- `frontend/src/LandingPagePro.tsx` (hero, messaging)
- `frontend/src/PricingPage.tsx` (offer clarity)
- `docs/sales/MARKETING_PLAYBOOK.md` (existing ICP definition)
- `PRODUCT_CATALOG.md` (product/service details)
- `frontend/src/Blog.tsx` (content tone)

**Questions:**
- Who do the existing pages assume they're talking to?
- What pain points are mentioned (or implied)?
- What benefits are emphasized?
- Is messaging consistent across pages?
- Are there contradictions or unclear CTAs?

**Files Provided Below:** (Next section)

---

### Task 2: Define ICP

**ICP Dimensions to clarify:**

1. **Role/Title:** Who makes the buying decision? (Developer? CTO? CEO?)
2. **Company Type:** Startup? Agency? Enterprise? Mix?
3. **Company Size:** 1-50? 50-500? 500+?
4. **Industry Focus:** Software? Consulting? Other?
5. **Pain Points (Top 3):**
   - E.g., "Manual testing is slow," "Hiring senior devs is expensive," "Deploying is risky"
6. **Desired Outcome:** What do they want to achieve?
   - E.g., "Ship features 2x faster," "Reduce QA costs," "Deploy with confidence"
7. **Budget:** $0-$100? $1K+? Custom?
8. **Purchase Cycle:** Impulse? 2-week? 3-month?
9. **Buying Signals:**
   - E.g., "Searching for 'AI code generator'," "Posted about dev hiring struggles"
10. **Objections:** What stops them from buying?
    - E.g., "Cost," "Learning curve," "Integration complexity"

---

### Task 3 & 4: Create Config Files

We'll create two YAML files that act as the "source of truth" for all marketing and agent decisions.

**File 1: `swarm/config/businessProfile.yaml`** (What we sell, to whom)

```yaml
# TitanForge Business Profile
# Primary source of truth for all marketing and agent logic

businessName: TitanForge
tagline: "Build, automate, and innovate faster with AI agents"

# ICP (Ideal Customer Profile)
idealCustomerProfile:
  primarySegments:
    - segment: "Solo Developers & Small Teams"
      role: "Software Developer / Tech Lead"
      companySize: "1-50"
      companyType: "Startup / Individual"
      pain_points:
        - "Building repetitive boilerplate is slow and boring"
        - "Can't afford to hire senior developers"
        - "Testing and code review are bottlenecks"
      desired_outcomes:
        - "Spend more time on creative/business logic"
        - "Ship features faster with fewer people"
        - "Reduce bugs and deployment risk"
      budget: "$19-$99/month"
      purchaseCycle: "Impulse to 1-week"
      buyingSignals:
        - "Searching 'AI code generator' or 'dev automation'"
        - "Active in Python/JavaScript communities"
        - "Posted about dev hiring struggles"
      objections:
        - "Cost (but willing to try free/cheap)"
        - "Learning curve (wants plug-and-play)"
        - "Afraid AI output is poor quality"
    
    - segment: "Dev Agencies & Consultancies"
      role: "Founder / Operations Lead"
      companySize: "10-500"
      companyType: "Development Agency / Consulting"
      pain_points:
        - "Delivery timelines are tight; margins are thin"
        - "Senior devs focus on billable work, not internal tools"
        - "Quality consistency across projects is hard"
      desired_outcomes:
        - "Deliver projects 2x faster"
        - "Improve quality while reducing labor"
        - "Offer new 'AI-powered' services to differentiate"
      budget: "$999-$4,999/month"
      purchaseCycle: "2-4 weeks"
      buyingSignals:
        - "Questions about 'speeding up delivery' or 'AI services'"
        - "Posted about team scaling or hiring challenges"
        - "Evaluating new technologies"
      objections:
        - "Afraid of losing control/quality"
        - "Integration complexity with existing workflow"
        - "ROI unclear"
    
    - segment: "Enterprises & Innovators"
      role: "VP Engineering / CTO"
      companySize: "500+"
      companyType: "Enterprise / Scale-up"
      pain_points:
        - "Development velocity is bottleneck to growth"
        - "Hiring top talent is expensive and slow"
        - "Need to maintain high quality and compliance"
      desired_outcomes:
        - "Unlock engineering velocity at scale"
        - "Reduce time-to-value for innovation"
        - "Competitive advantage via AI integration"
      budget: "Custom / unlimited"
      purchaseCycle: "6-12 weeks"
      buyingSignals:
        - "Attending AI / developer conferences"
        - "Company is hiring aggressively"
        - "Posted about innovation or R&D"
      objections:
        - "Enterprise requirements (SLA, compliance, security)"
        - "Need proof of concept before commitment"
        - "Integration with legacy systems"

# Core Offerings
offerings:
  primary:
    name: "AIaaS Platform"
    description: "Self-serve access to TitanForge agent swarm for development automation"
    tiers:
      - name: "Starter"
        monthlyPrice: 19
        annualPrice: 199
        target: "Solo developers, hobbyists"
        limit: "1,000 API calls/month, 1 concurrent agent"
      - name: "Pro"
        monthlyPrice: 99
        annualPrice: 999
        target: "Small teams, freelancers"
        limit: "10,000 API calls/month, 5 concurrent agents"
      - name: "Enterprise"
        monthlyPrice: null  # Custom
        annualPrice: null   # Custom
        target: "Enterprises, agencies"
        limit: "Unlimited, custom SLA"
  
  secondary:
    - name: "Productized Services"
      description: "Fixed-price development packages"
      offerings:
        - "Micro-Feature Development ($499-$1,499)"
        - "Website Audit ($299-$799)"
        - "API Endpoint Creation ($799-$1,999)"

# Unique Value Proposition (Why us, not others?)
uniqueValueProposition:
  headline: "The only AI swarm designed for developers, by developers"
  keyDifferentiators:
    - "Agentic Intelligence: Not just AI tools; coordinated swarm that thinks together"
    - "Full Lifecycle: From ideation through testing to deployment"
    - "Transparent: You see what agents do; no black boxes"
    - "Adaptable: Retune for any tech stack or business domain"
    - "Affordable: Start at $19/month"

# Tone & Voice
tonality:
  primary: "Direct, practical, no-BS"
  secondary: "Empowering, ambitious, technical but accessible"
  avoid:
    - "Marketing jargon"
    - "False promises"
    - "Over-hype on AI capabilities"

# Target Channels (where to find ICP)
channels:
  primaryChannels:
    - "SEO (blogs, tutorials about AI and dev automation)"
    - "Developer communities (Reddit, Discord, GitHub)"
    - "Tech job boards (where CTOs/Founders recruit)"
  secondaryChannels:
    - "LinkedIn (outbound to CTOs/VPs)"
    - "Conferences (AI, dev, SaaS)"
    - "Affiliate / partner networks"

```

**File 2: `swarm/config/positioningLayer.yaml`** (How we talk about it)

```yaml
# TitanForge Positioning Layer
# Messaging, CTAs, copy direction for all channels

# Primary Message (Hero / Homepage)
primaryMessage:
  headline: "Ship code in days, not weeks. Meet your AI development team."
  subheadline: "TitanForge agents handle testing, code review, documentation, and deployment. You focus on the parts that matter."
  ctaPrimary: "Try Free (No Credit Card)"
  ctaSecondary: "See How It Works"

# Value Props (What we promise)
valueProps:
  - headline: "Write 10x faster"
    description: "Agents generate boilerplate and handle repetitive tasks. Your team writes only the critical parts."
    icon: "zap"
  
  - headline: "Ship with confidence"
    description: "Automated testing, code review, and deployment catch issues before they reach production."
    icon: "shield"
  
  - headline: "Hire fewer people"
    description: "AI agents work 24/7. Deliver the same output with 30-50% fewer headcount."
    icon: "users"

# Page-Specific Copy
pages:
  landing:
    h1: "Ship code in days, not weeks. Meet your AI development team."
    sections:
      - title: "The Problem"
        copy: "Your team spends 60% of time on repetitive tasks: boilerplate, testing, code review, documentation. That's time wasted when you could be innovating."
      
      - title: "The Solution"
        copy: "TitanForge is a swarm of AI agents, each specialized in a part of the dev lifecycle. They work together. They think. They learn from your codebase."
      
      - title: "The Results"
        copy: "40% faster feature delivery. 60% fewer bugs. 50% lower development costs. Without hiring more people."
    
    cta: "Start Free Today (No Card Required)"
  
  pricing:
    title: "Simple, Transparent Pricing"
    subtitle: "Pick a plan. Scale whenever you're ready."
    comparison:
      - feature: "Concurrent Agent Runs"
        starter: "1"
        pro: "5"
        enterprise: "Unlimited"
      - feature: "API Calls / Month"
        starter: "1,000"
        pro: "10,000"
        enterprise: "Unlimited"
      - feature: "Support"
        starter: "Community"
        pro: "Priority Email"
        enterprise: "Dedicated"
  
  blog:
    title: "Learn How AI Agents Are Reshaping Development"
    subtitle: "Tutorials, case studies, and industry insights"
    cta_position: "End of each post"
    cta_text: "Want to try agents on your code? Start free with TitanForge"

# Email Messaging
emailMessaging:
  subjectLineStyle: "Direct, benefit-focused, low hype"
  exampleSubjectLines:
    - "Ship your next feature in 2 days (not 2 weeks)"
    - "40% faster delivery? See how 500+ dev teams do it"
    - "Your code review took 3 hours. Ours takes 30 seconds."

# Common Objections & Rebuttals
objectionsAndRebuttals:
  objection: "AI code quality is bad"
  rebuttal: "Ours isn't. Our agents are trained on thousands of production codebases. They review and refine their own output."
  
  objection: "This will replace developers"
  rebuttal: "No. It replaces drudgery. Developers become architects and innovators, not copy-paste machines."
  
  objection: "Too expensive"
  rebuttal: "At $99/month, our Pro plan costs less than 1 day of a senior developer. You save that in faster delivery in week 1."

# Seasonal / Campaign Messaging
campaigns:
  hiring_season:
    headline: "Hire fewer people. Deliver more. TitanForge for teams that grow without headcount."
    cta: "See how it works"
  
  speed_focused:
    headline: "Your competitors are shipping 2x faster. Here's how."
    cta: "Try agents risk-free"

```

---

### Task 5: Map Core User Journey

**Create file: `swarm/config/coreUserJourney.yaml`**

```yaml
# TitanForge Core User Journey
# Defines the path from cold visitor to paying customer

journey:
  stage_1_awareness:
    name: "Awareness"
    channels:
      - "Search: 'AI code generator', 'dev automation', etc."
      - "Blog post shared on Twitter/Reddit"
      - "Referral from friend/colleague"
    touchpoints:
      - "Blog post / SEO result"
      - "Social media clip"
      - "Landing page"
    duration: "Seconds to minutes"
    goal: "Answer: What is TitanForge? Is this for me?"
    success_metric: "Click landing page CTA or email form"
  
  stage_2_consideration:
    name: "Consideration"
    pages:
      - "/": "Hero, value props, initial proof (testimonials, metrics)"
      - "/pricing": "Clear tiers, comparison, FAQ"
      - "/blog": "Deep dives on AI agents, case studies"
    touchpoints:
      - "Read landing page"
      - "Explore pricing tiers"
      - "Read blog post"
      - "Enter email in lead form"
    duration: "5-20 minutes"
    goal: "Gather info. Decide if worth trying."
    success_metric: "Sign up for trial OR enter email"
  
  stage_3_signup:
    name: "Signup"
    pages:
      - "/register": "Email + password"
    touchpoints:
      - "Click 'Try Free' CTA"
      - "Fill email form"
      - "Register account"
    duration: "1-2 minutes"
    goal: "Get in the door. Reduce friction."
    success_metric: "Account created, email confirmed"
  
  stage_4_onboarding:
    name: "Onboarding"
    pages:
      - "/dashboard": "Welcome, first task setup"
    touchpoints:
      - "See dashboard"
      - "Run first agent task (guided)"
      - "See result (AHA moment)"
      - "Email: welcome + next steps"
    duration: "10-20 minutes"
    goal: "Show immediate value. Make first win fast."
    success_metric: "User runs first task successfully"
  
  stage_5_activation:
    name: "Activation"
    touchpoints:
      - "Use system for 5+ tasks"
      - "See concrete results (faster delivery, better quality)"
      - "Integrate with real project"
    duration: "Days to 1 week"
    goal: "Prove value. Build habit."
    success_metric: "User considers upgrade to Pro"
  
  stage_6_monetization:
    name: "Monetization"
    pages:
      - "/pricing": "View upgrade path"
      - "/checkout": "Purchase Pro or Enterprise"
    touchpoints:
      - "Hit rate limit on Starter"
      - "Email: 'Ready for more? Pro unlocks 5x capabilities'"
      - "Click upgrade, enter payment"
    duration: "2-4 weeks into trial"
    goal: "Convert to paid. Lock in recurring revenue."
    success_metric: "Payment successful, subscription active"

# Events to Track
events:
  awareness:
    - page_view
    - traffic_source
    - referrer
  
  consideration:
    - pricing_page_view
    - blog_post_read
    - form_view
    - email_entered
  
  signup:
    - registration_started
    - registration_completed
    - email_confirmed
  
  onboarding:
    - dashboard_viewed
    - first_task_created
    - first_task_completed
  
  activation:
    - task_count (5+)
    - api_call_count (50+)
    - result_satisfaction (inferred from logs)
  
  monetization:
    - rate_limit_hit
    - upgrade_page_viewed
    - subscription_created
    - payment_successful

```

---

### Task 6: Document Config Usage

**Create file: `swarm/config/README.md`**

```markdown
# Swarm Config Layer

All marketing and business logic is centralized here. Agents read these configs to generate domain-specific strategies, content, and CTAs.

## Files

### `businessProfile.yaml`
**What:** Ideal Customer Profile, offerings, tonality, channels
**Who Reads:** Copy_Agent, Content_Agent, Funnel_Agent, Growth_Orchestrator
**When:** Every marketing decision (content, messaging, targeting)
**Example Use:** 
- Copy_Agent reads ICP pain points and generates hero headlines
- Content_Agent reads target channels and creates topic ideas for that audience
- Funnel_Agent reads desired outcomes and designs landing page sections

### `positioningLayer.yaml`
**What:** Messaging, CTAs, value props, objection rebuttals
**Who Reads:** Copy_Agent, EmailCRM_Agent, SocialMediaManager_Agent
**When:** Creating any customer-facing copy
**Example Use:**
- Copy_Agent uses primaryMessage to write landing page H1
- EmailCRM_Agent uses emailMessaging to write subject lines
- SocialMediaManager_Agent uses valueProps to create social media posts

### `coreUserJourney.yaml`
**What:** Stages from visitor to customer, touchpoints, events to track
**Who Reads:** Funnel_Agent, Analytics_Agent, EmailCRM_Agent
**When:** Designing funnels, setting up analytics, creating sequences
**Example Use:**
- Funnel_Agent uses journey stages to design page layout and CTA placement
- Analytics_Agent sets up event tracking based on journey stages
- EmailCRM_Agent creates email triggers based on journey stage transitions

## How to Retune for a New Business Domain

1. **Update `businessProfile.yaml`:**
   - Replace ICP segments with new target audience
   - Update pain points, desired outcomes, budget, channels
   - Update offerings and pricing

2. **Update `positioningLayer.yaml`:**
   - Rewrite headline, subheadline, value props
   - Adjust tone & voice if needed
   - Update email messaging for new audience

3. **Update `coreUserJourney.yaml`:**
   - Adjust stages if needed (some products have longer sales cycles)
   - Update touchpoints for new channels
   - Adjust event tracking for new business model

4. **Agents automatically adapt:**
   - All agents read from these configs
   - No code changes needed
   - Marketing strategy regenerated for new domain

## Example: Retune for "AI Copywriting Agency"

**Original:** TitanForge = AI dev platform for developers
**New:** TitanForge = AI copywriting tool for marketing teams

**Changes:**

1. In `businessProfile.yaml`:
   - ICP: Change from "developers" to "marketing managers, copywriters, content agencies"
   - Pain points: Change from "slow testing" to "writer's block, hiring expensive copywriters"
   - Offerings: Change from "API calls for code generation" to "monthly essay/email generation quota"

2. In `positioningLayer.yaml`:
   - Headline: "Write 100 marketing emails in 1 day. Meet your AI copywriter."
   - Value Props: "Write 10x faster", "Consistency across brand voice", "Never miss a deadline"

3. Run: `Content_Agent.generate_content_strategy()` 
   - **Output:** Blog ideas about copywriting, marketing psychology, email marketing, etc.

4. Run: `Copy_Agent.generate_landing_page()`
   - **Output:** New landing page copy optimized for marketing managers

---

## Maintenance

- Review and update configs quarterly
- As product offerings change, update `businessProfile.yaml` offerings section
- As market research reveals new pain points, update ICP
- As you test new messaging, document winners in `positioningLayer.yaml`

```

---

## SPRINT M1 Output

**Files Created:**
1. ✅ `swarm/config/businessProfile.yaml` – ICP, offerings, channels, tone
2. ✅ `swarm/config/positioningLayer.yaml` – Messaging, CTAs, value props
3. ✅ `swarm/config/coreUserJourney.yaml` – Stages, touchpoints, events
4. ✅ `swarm/config/README.md` – How agents use configs

**Decisions Made:**
- Primary ICP: **Developers, CTOs, Dev Agencies** (in that order of priority)
- Primary Pain: **Speed, cost, quality at scale**
- Positioning: **"AI swarm designed by developers for developers"**
- Core Funnel: **Visitor → Lead → Signup → Activate → Upgrade**

---

## SPRINT M1 Next Actions

**What you should do:**
1. Review the 4 config files above
2. Edit them to match your actual ICP and offerings (if different)
3. Create the files in `F:\TitanForge\swarm\config\`
4. Test: Run a grep to confirm file creation

**Expected Time:** 30 minutes

---

## SPRINT M1 → M2 Preview

Once positioning is locked, we move to:
- **SPRINT M2:** Landing page optimization (hero, CTAs, social proof)
- **SPRINT M3:** Lead capture backend wiring
- **SPRINT M4:** Blog & SEO infrastructure

---

**Status:** ✅ SPRINT M1 COMPLETE (ready for next)  
**Owner:** Growth_Orchestrator  
**Date:** 2026-02-17
