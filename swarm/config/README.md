# Swarm Configuration Layer

All marketing, business, and customer acquisition logic is **centralized here**. Agents read these configs to generate domain-specific strategies, content, messaging, and funnels.

**Primary Mission:** Make TitanForge adaptable to any business domain with zero code changes.

---

## Files Overview

### 1. `businessProfile.yaml`
**What:** Ideal Customer Profile, offerings, pricing, channels, market context  
**Who Reads:** Copy_Agent, Content_Agent, Funnel_Agent, Growth_Orchestrator, EmailCRM_Agent  
**Read Frequency:** Every marketing decision (content, messaging, audience targeting)

**Key Sections:**
- `idealCustomerProfile`: 3 segments (Solo Devs, Agencies, Enterprise) with pain points, desired outcomes, budget, buying signals
- `offerings`: AIaaS platform tiers + productized services
- `uniqueValueProposition`: Why TitanForge, not alternatives
- `channels`: Where to find ICP (SEO, communities, LinkedIn, etc.)
- `successMetrics`: Month 1, Month 3, Month 6 targets

**Example Use:**
- Copy_Agent reads ICP pain points → generates hero headlines around those pain points
- Content_Agent reads target channels → creates blog topics for those audiences
- Funnel_Agent reads desired outcomes → designs landing page sections to address outcomes
- EmailCRM_Agent reads objections → crafts email rebuttals

---

### 2. `positioningLayer.yaml`
**What:** Messaging frameworks, CTAs, value props, objection rebuttals, social media hooks  
**Who Reads:** Copy_Agent, EmailCRM_Agent, SocialMediaManager_Agent  
**Read Frequency:** When creating any customer-facing copy (landing page, emails, ads, posts)

**Key Sections:**
- `primaryMessage`: Hero headline, subheadline, CTAs
- `valueProps`: 4 core benefits with stats
- `pages`: Detailed copy frameworks for landing, pricing, blog pages
- `emailMessaging`: Subject line style, example sequences, tone
- `objectionsAndRebuttals`: Common objections + responses
- `campaigns`: Seasonal/campaign-specific messaging
- `socialMediaHooks`: Twitter, LinkedIn, Reddit content hooks
- `adCopyTemplates`: Search and social ad copy

**Example Use:**
- Copy_Agent uses `primaryMessage` → writes landing page H1
- EmailCRM_Agent uses `emailMessaging` → writes welcome sequence subject lines
- SocialMediaManager_Agent uses `socialMediaHooks` → posts daily content
- Sales_Agent uses `objectionsAndRebuttals` → handles customer objections

---

### 3. `coreUserJourney.yaml`
**What:** User journey stages, touchpoints, events to track, funnel conversion rates, A/B test ideas  
**Who Reads:** Funnel_Agent, Analytics_Agent, EmailCRM_Agent  
**Read Frequency:** When designing funnels, setting up analytics, creating sequences

**Key Sections:**
- `journey`: 9 stages (Awareness → Consideration → Lead → Signup → Onboarding → Activation → Monetization → Expansion → Retention)
- For each stage: User questions, pages visited, success metrics, conversion targets
- `events`: Full event tracking map per stage (100+ events)
- `optimization_levers`: What to test/change to improve conversion
- `ab_tests`: Priority experiments (hero headline, form length, CTA copy, etc.)
- `retention`: Post-purchase customer health metrics

**Example Use:**
- Funnel_Agent uses journey stages → designs page layout and CTA placement for each stage
- Analytics_Agent uses events map → configures GA4 event tracking and dashboards
- EmailCRM_Agent uses email triggers → creates sequences at each stage transition
- Growth_Orchestrator uses conversion targets → prioritizes optimization efforts

---

## How to Use Configs

### For Development (Frontend/Backend)

**Read businessProfile.yaml:**
```javascript
// Frontend example: Use ICP to customize landing page
const icp = businessProfile.idealCustomerProfile.primarySegments[0]; // Solo Devs
const painPoints = icp.pain_points;  // ["Building boilerplate is slow", ...]
// Render landing page sections focused on these pain points
```

**Read positioningLayer.yaml:**
```javascript
// Use copy frameworks to populate landing page
const copyFramework = positioningLayer.pages.landing;
const heroHeadline = copyFramework.sections[0].headline;
const ctaPrimary = copyFramework.cta_primary;
// Render hero section with this copy
```

**Read coreUserJourney.yaml:**
```javascript
// Track events in analytics
const events = coreUserJourney.events;
const signupEvents = events.stage_5_signup;  // ['registration_started', 'registration_completed', ...]
// Send these events to GA4
```

---

### For Agents (Content Generation, Copy, Email, etc.)

**Copy_Agent workflow:**
1. Read `businessProfile.yaml` → ICP pain points, tonality
2. Read `positioningLayer.yaml` → primary message, value props
3. Generate: Landing page headlines, email subject lines, blog titles

**Content_Agent workflow:**
1. Read `businessProfile.yaml` → channels, keywords
2. Read `coreUserJourney.yaml` → user questions at each stage
3. Generate: Blog post ideas, tutorials, case studies addressing those questions

**EmailCRM_Agent workflow:**
1. Read `businessProfile.yaml` → objections
2. Read `positioningLayer.yaml` → email messaging frameworks
3. Read `coreUserJourney.yaml` → email triggers, conversion targets
4. Generate: Welcome sequence, nurture sequence, objection-handling emails

**Funnel_Agent workflow:**
1. Read `coreUserJourney.yaml` → journey stages, conversion targets
2. Read `positioningLayer.yaml` → value props, CTAs
3. Generate: Page layouts, CTA placement, form design, success metrics

**Analytics_Agent workflow:**
1. Read `coreUserJourney.yaml` → events map, funnel stages
2. Generate: GA4 event configuration, custom dashboards, tracking code

---

## How to Retune for a New Business Domain

**Scenario:** You want to use TitanForge for "AI Copywriting Agency" instead of "AI Dev Platform"

### Step 1: Update `businessProfile.yaml`

Replace ICP segments:
```yaml
# OLD (Developers)
primarySegments:
  - segment: "Solo Developers & Small Teams"

# NEW (Copywriting Agency)
primarySegments:
  - segment: "Marketing Managers & Content Teams"
    role: "Content Manager, Head of Marketing, Copywriter"
    pain_points:
      - "Writer's block and creativity fatigue"
      - "Hiring experienced copywriters is expensive"
      - "Consistency across brand voice is hard"
```

Update offerings:
```yaml
# OLD (API calls, concurrent agents)
offerings:
  primary:
    name: "AIaaS Platform"
    tiers:
      - name: "Starter"
        monthlyPrice: 19
        limit: "1,000 API calls/month, 1 concurrent agent"

# NEW (Essay/email generation quota)
offerings:
  primary:
    name: "AI Copywriting Platform"
    tiers:
      - name: "Starter"
        monthlyPrice: 29
        limit: "50 essays/month, unlimited emails"
```

### Step 2: Update `positioningLayer.yaml`

Rewrite messaging:
```yaml
# OLD
primaryMessage:
  headline: "Ship code in days, not weeks. Meet your AI development team."

# NEW
primaryMessage:
  headline: "Write 100 marketing emails in 1 day. Meet your AI copywriter."

# Update value props
valueProps:
  - headline: "Write 10x faster"
    description: "Agents generate copy in seconds. No more blank page syndrome."
  - headline: "Consistent brand voice"
    description: "Every email, every landing page, same tone and quality."
  - headline: "Ship more campaigns"
    description: "Monthly campaign output increases 5x. Deadlines met, clients happy."
```

### Step 3: Update `coreUserJourney.yaml`

Adjust user journey stages if needed:
```yaml
# Most of the journey stays same (awareness → consideration → lead → signup → ...)
# But update specific touchpoints and content

stage_2_consideration:
  touchpoints:
    - "Read landing page hero and copy samples"
    - "Explore pricing tiers and essay/email quotas"
    - "Read case studies (e.g., 'How MarketingCo wrote 500 emails in Q3')"
    - "See template library or examples"
```

### Step 4: Agents Automatically Adapt

**No code changes needed.** All agents read from configs:

```
Update configs → Save → Run Content_Agent.generate_strategy()
Output: New blog topics, landing page copy, email sequences optimized for copywriting niche
```

### Step 5: Test New Domain

1. Verify frontend renders new copy correctly
2. Check email sequences trigger properly
3. Test analytics events fire correctly
4. Monitor conversion rates (should see different patterns for different ICP)

---

## Best Practices

### 1. Keep Configs DRY (Don't Repeat Yourself)

If you need to reference something in multiple configs, create a variable and reference it:

```yaml
# In businessProfile.yaml
uniqueValueProposition:
  headline: "The only AI swarm designed for developers, by developers"

# In positioningLayer.yaml
# DON'T repeat the headline; reference it or keep it consistent
primaryMessage:
  headline: "[Same as businessProfile.uniqueValueProposition.headline]"
```

### 2. Update Quarterly

- Review conversion metrics against `coreUserJourney.yaml` targets
- If missing targets, update and test
- As product features change, update `offerings` section
- As market research reveals new pain points, update ICP

### 3. Version Control

- Commit all config changes to Git
- Use commit messages like: "Update ICP for enterprise segment" or "Test new hero copy"
- Easy to rollback if a change tanks metrics

### 4. Document Changes

When you update a config, note why:
```yaml
# Example comment in config file
# CHANGED: 2026-02-20 - Testing lower price point for Starter tier
# REASON: Improve consideration → lead conversion
# EXPECTED: 15% increase in free trial signups
offerings:
  primary:
    tiers:
      - name: "Starter"
        monthlyPrice: 19  # Was $29
```

### 5. Test Hypotheses Systematically

Use `ab_tests` section in `coreUserJourney.yaml` to guide experimentation:
```yaml
ab_tests:
  test_1:
    name: "Hero Headline Test"
    hypothesis: "Benefit-driven headline increases CTR"
    control: "Current headline"
    variant: "New headline"
    metric: "Hero CTA click rate"
    # Run this test for 2 weeks, measure, document winner
```

---

## Integration Checklist

- [ ] Confirm all config files exist and are valid YAML
- [ ] Frontend loads `businessProfile.yaml` and `positioningLayer.yaml` for dynamic content
- [ ] Backend tracks events from `coreUserJourney.yaml` to GA4 or custom analytics
- [ ] Agents have read access to all config files
- [ ] Marketing team has process to update configs quarterly
- [ ] All YAML is version-controlled in Git
- [ ] Documentation (this README) is kept current

---

## Questions?

**For agents:** Each agent has specific sections of configs they read. See "Who Reads" section above.

**For humans:** Update configs directly. Changes take effect immediately (no deploy needed for marketing changes).

**For new domains:** Follow "How to Retune for a New Business Domain" steps above.

---

**Last Updated:** 2026-02-17  
**Owner:** Growth_Orchestrator  
**Status:** ✅ ACTIVE - Used by all marketing agents
