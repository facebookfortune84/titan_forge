# VOICE OUTREACH SYSTEM – MASTER DESIGN & SPRINT PLAN

**Orchestrator Mode:** 🔴 VOICE + MINIMAL INPUT ACTIVE  
**Date:** 2026-02-17 · **Timestamp:** 04:35 UTC  
**Status:** Ready for Sprint Execution  

---

## 🎯 VOICE SYSTEM OBJECTIVES

### What We're Building
A complete **automation-ready voice outreach layer** that:
- Designs call flows, scripts, and conversation state machines
- Defines follow-up cadences (calls + SMS + email)
- Maps to TitanForge backend for CRM/event tracking
- Respects compliance, consent, and time-of-day rules
- Requires NO actual phone dialing (logic-only)
- Integrates with external telephony (Asterisk, FreeSWITCH, Twilio, etc.)

### What We're NOT Building
- Actual phone dialer or SIP server
- Real calling or SMS sending
- Bypassing consent or do-not-call rules
- External communication without human review

---

## 📋 SPRINT SEQUENCE (V1-V6 + HYPER TUNING)

### SPRINT V1 – Voice Business Profile & Campaign Map
**Owner:** VoiceStrategy_Agent + Growth_Orchestrator  
**Duration:** 2-3 hours  
**Deliverables:**
- `swarm/voice/businessProfile.json` – Voice-specific ICP segments, pain points, objections
- `swarm/voice/campaigns.json` – Map of all voice campaigns (what, who, when, why)
- `swarm/voice/README_V1.md` – Voice system overview

**What it answers:**
- Who do we call? (Which leads/customers/segments)
- Why do we call? (What outcome are we trying to achieve)
- When do we call? (Timing, triggers, cadence)
- What do we say? (Tone, messaging, pain point focus)

**Files:**
```
swarm/voice/
├─ businessProfile.json
├─ campaigns.json
├─ README_V1.md
```

---

### SPRINT V2 – Call Scripts (New Lead, Trial, Renewal, Winback)
**Owner:** VoiceScript_Agent  
**Duration:** 4-6 hours  
**Deliverables:**
- `swarm/voice/scripts/new_lead_welcome.md` – For newly captured leads
- `swarm/voice/scripts/trial_expiring_upsell.md` – For trial users nearing renewal
- `swarm/voice/scripts/customer_renewal_check.md` – For existing customers
- `swarm/voice/scripts/winback_inactive.md` – For churned/dormant customers
- `swarm/voice/scripts/objection_handling.md` – Common rebuttals

**What each script includes:**
- Opening: Identification + consent + intent
- Engagement: Pain point validation + qualification
- Pitch: Tailored value prop + offer
- Objection Handling: Common objections + rebuttals
- Closing: Clear CTA (book demo, upgrade, renew) + next step

**Files:**
```
swarm/voice/scripts/
├─ new_lead_welcome.md
├─ trial_expiring_upsell.md
├─ customer_renewal_check.md
├─ winback_inactive.md
├─ objection_handling.md
```

---

### SPRINT V3 – Call Flows (State Machines in JSON)
**Owner:** VoiceFlow_Agent  
**Duration:** 4-6 hours  
**Deliverables:**
- `swarm/voice/flows/new_lead_qualification.json` – State machine for new lead calls
- `swarm/voice/flows/trial_expiring_followup.json` – State machine for trial upsell calls
- `swarm/voice/flows/customer_checkin.json` – State machine for customer health checks
- `swarm/voice/flows/winback_campaign.json` – State machine for reactivation calls

**What each flow includes:**
- Nodes: Message, question, decision, transfer, hang up
- Edges: Answer-based routing (yes/no/maybe/transfer)
- Variables: Inputs from CRM (name, company, trial status)
- Exit conditions: Appointment scheduled, opt-out, call dropped
- Error handling: No answer, system failure, transfer

**Format (JSON State Machine):**
```json
{
  "id": "new_lead_qualification",
  "name": "New Lead Qualification Call",
  "nodes": [
    {
      "id": "start",
      "type": "message",
      "script": "Hi {{first_name}}, this is {{agent_name}} from TitanForge..."
    },
    {
      "id": "ask_company",
      "type": "question",
      "script": "Quick question – what's your main dev challenge right now?"
    }
  ],
  "edges": [
    {
      "from": "start",
      "to": "ask_company",
      "condition": "call_answered"
    }
  ]
}
```

**Files:**
```
swarm/voice/flows/
├─ new_lead_qualification.json
├─ trial_expiring_followup.json
├─ customer_checkin.json
├─ winback_campaign.json
```

---

### SPRINT V4 – Follow-up Cadences & Timing Rules
**Owner:** VoiceCadence_Agent  
**Duration:** 3-4 hours  
**Deliverables:**
- `swarm/voice/cadences/saas_default.json` – Standard 3-call cadence for leads
- `swarm/voice/cadences/enterprise_aggressive.json` – More frequent for high-value
- `swarm/voice/cadences/retention_light.json` – Low-frequency for existing customers
- `swarm/voice/cadences/winback_sequence.json` – Reactivation sequence

**What each cadence includes:**
- Steps: Array of {day, type (CALL/SMS/EMAIL), flow_ref, conditions}
- Rules: Stop if opted out, do-not-call, no answer after N attempts
- Escalation: When to transfer to sales team
- Success criteria: When to mark campaign as complete

**Format (JSON Cadence):**
```json
{
  "id": "saas_default",
  "name": "SaaS Default 3-Call Cadence",
  "steps": [
    {
      "day": 0,
      "type": "CALL",
      "flow_ref": "new_lead_qualification",
      "condition": "lead_created",
      "time_window": "09:00-17:00"
    },
    {
      "day": 2,
      "type": "CALL",
      "flow_ref": "new_lead_qualification",
      "condition": "call_1_no_answer OR call_1_not_interested",
      "time_window": "10:00-18:00"
    },
    {
      "day": 5,
      "type": "EMAIL",
      "template_ref": "nurture_email_1",
      "condition": "all_calls_no_answer"
    }
  ],
  "stop_conditions": [
    "opted_out",
    "on_dnc_list",
    "3_calls_no_answer",
    "explicit_decline"
  ]
}
```

**Files:**
```
swarm/voice/cadences/
├─ saas_default.json
├─ enterprise_aggressive.json
├─ retention_light.json
├─ winback_sequence.json
```

---

### SPRINT V5 – CRM & Event Integration Schema
**Owner:** VoiceCRM_Agent  
**Duration:** 3-4 hours  
**Deliverables:**
- `swarm/voice/integrationSchema.md` – Complete spec for backend integration
- `swarm/voice/events.json` – All voice-related events and their payloads
- `swarm/voice/leads_schema.json` – Lead record fields needed for voice
- `swarm/voice/voice_log_schema.json` – Call log structure

**What it includes:**
- Events: CALL_PLACED, CALL_ANSWERED, LEAD_QUALIFIED, APPOINTMENT_BOOKED, OPTED_OUT, etc.
- Fields: What data is needed before/during/after calls
- Payloads: Exact JSON to send to backend after each event
- Endpoints: Which backend endpoints to hit
- Error handling: How to handle failed integrations

**Example Event Schema:**
```json
{
  "event": "CALL_COMPLETED",
  "timestamp": "2026-02-17T10:30:00Z",
  "lead_id": "lead_12345",
  "call_id": "call_abcde",
  "flow_id": "new_lead_qualification",
  "result": "qualified",
  "duration": 420,
  "notes": "User interested in trial",
  "next_step": "send_trial_link",
  "backend_endpoint": "POST /api/v1/leads/{lead_id}/voice_events",
  "payload": {
    "event_type": "CALL_COMPLETED",
    "call_duration": 420,
    "result": "qualified",
    "notes": "User interested in trial"
  }
}
```

**Files:**
```
swarm/voice/
├─ integrationSchema.md
├─ events.json
├─ leads_schema.json
├─ voice_log_schema.json
```

---

### SPRINT V6 – Compliance Review & Refinement
**Owner:** VoiceCompliance_Agent  
**Duration:** 2-3 hours  
**Deliverables:**
- `swarm/voice/compliance.md` – Legal + ethical guidelines
- Updated flows with:
  - Clear identification at start
  - Easy opt-out language
  - Time-of-day enforcement
  - Do-not-call checks
- `swarm/voice/testing_checklist.md` – Manual QA steps before deployment

**What it covers:**
- Consent and opt-in verification
- Clear identification ("Hi, this is X from Y")
- Easy way to opt out ("Say STOP to remove from list")
- Time-of-day rules (no calls before 8am, after 9pm)
- Do-not-call registry checks
- Transparent about what we're offering
- No deception or manipulation

**Files:**
```
swarm/voice/
├─ compliance.md
├─ testing_checklist.md
├─ (updated flows with compliance annotations)
```

---

## 🚀 WHAT VOICE SYSTEM ENABLES

Once complete (V1-V6), the system supports:

✅ **Outbound campaigns:**
- New leads: Warm welcome + qualification
- Trial users: Upsell before expiry
- Customers: Health checks + expansion
- Churned: Win-back sequences

✅ **Inbound routing (if applicable):**
- IVR logic for common queries
- Transfer to human sales team
- Schedule callbacks

✅ **Follow-up automation:**
- Call cadences (Day 0, Day 2, Day 5, etc.)
- Multi-channel escalation (Call → SMS → Email)
- Opt-out respect and enforcement

✅ **Data integration:**
- Every call event logged to CRM
- Lead progression tracked
- Conversion metrics captured
- A/B testing ready

✅ **Compliance:**
- All calls documented
- Opt-out honored
- Time windows enforced
- Do-not-call respected

---

## 🎭 AGENT ROLES (Voice Layer)

New agents added to roster:

| Agent | Role | Reads | Writes |
|-------|------|-------|--------|
| VoiceStrategy_Agent | Designs campaigns, segments, timing | businessProfile, coreUserJourney | campaigns.json, strategy docs |
| VoiceScript_Agent | Writes call scripts | businessProfile, objection rebuttals | scripts/*.md |
| VoiceFlow_Agent | Converts scripts to state machines | scripts | flows/*.json |
| VoiceCadence_Agent | Designs timing and follow-up | campaigns, conversion targets | cadences/*.json |
| VoiceCompliance_Agent | Reviews for legal/ethical compliance | flows, scripts | compliance.md, annotations |
| VoiceCRM_Agent | Designs event/data integration | backend schema | integrationSchema.md, events.json |
| VoiceOrchestrator | Coordinates voice agents | all voice configs | coordination logic |

---

## 📍 FILE STRUCTURE (Final)

```
swarm/voice/
├─ README.md                          ← Start here
├─ businessProfile.json               ← Voice-specific ICP + campaigns
├─ campaigns.json                     ← Campaign map (what, who, when, why)
├─ compliance.md                      ← Legal/ethical guidelines
├─ integrationSchema.md               ← How to integrate with backend/dialer
├─ events.json                        ← All voice events and payloads
├─ leads_schema.json                  ← Required lead fields
├─ voice_log_schema.json              ← Call log structure
├─ testing_checklist.md               ← QA before deployment
├─ scripts/
│  ├─ new_lead_welcome.md
│  ├─ trial_expiring_upsell.md
│  ├─ customer_renewal_check.md
│  ├─ winback_inactive.md
│  └─ objection_handling.md
├─ flows/
│  ├─ new_lead_qualification.json
│  ├─ trial_expiring_followup.json
│  ├─ customer_checkin.json
│  └─ winback_campaign.json
└─ cadences/
   ├─ saas_default.json
   ├─ enterprise_aggressive.json
   ├─ retention_light.json
   └─ winback_sequence.json
```

---

## ⏱️ TIMELINE

| Sprint | Name | Duration | Cumulative |
|--------|------|----------|-----------|
| V1 | Business Profile & Campaigns | 2-3h | 2-3h |
| V2 | Call Scripts | 4-6h | 6-9h |
| V3 | Call Flows (State Machines) | 4-6h | 10-15h |
| V4 | Cadences & Timing | 3-4h | 13-19h |
| V5 | CRM/Event Integration | 3-4h | 16-23h |
| V6 | Compliance & Refinement | 2-3h | 18-26h |
| **Total Voice System** | **V1-V6** | **~20 hours** | **Ready for integration** |

---

## 🎯 NEXT STEP

**Ready to begin SPRINT V1?**

Reply with:
- ✅ "Begin SPRINT V1" → I'll create voice business profile & campaign map
- 🤔 "Review plan first" → I can refine this plan based on feedback
- 🚀 "Fast track to hyper tuning" → I'll create all V1-V6 files in parallel (more intensive)

---

**Status:** 🟡 AWAITING USER INPUT  
**Ready:** Yes, all sprints planned and ready to execute
