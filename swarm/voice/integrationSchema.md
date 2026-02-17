# Voice Outreach & CRM Integration Schema

## Overview
This document defines how TitanForge voice operations integrate with backend CRM and customer data systems.

## Lead Record Fields

### Required Fields
```json
{
  "leadId": "string (UUID)",
  "email": "string (required)",
  "firstName": "string",
  "lastName": "string",
  "phone": "string (required for voice)",
  "company": "string (optional)",
  "segment": "enum: solo_devs|agencies|enterprise",
  "status": "enum: cold|contacted|trial|customer|unresponsive",
  "createdAt": "ISO8601",
  "lastContactedAt": "ISO8601",
  "preferredContactTime": "string (e.g., 9am-5pm EST)",
  "doNotCall": "boolean",
  "doNotEmail": "boolean"
}
```

## Events & Backend Integration

### Event Payloads

**CALL_PLACED**
```json
{
  "eventType": "CALL_PLACED",
  "leadId": "string",
  "campaignId": "string",
  "timestamp": "ISO8601",
  "agentId": "string",
  "flowId": "string"
}
```

**CALL_ANSWERED**
```json
{
  "eventType": "CALL_ANSWERED",
  "leadId": "string",
  "campaignId": "string",
  "timestamp": "ISO8601",
  "callDuration": "seconds",
  "flowNodesTraversed": ["node1", "node2"]
}
```

**CALL_NO_ANSWER**
```json
{
  "eventType": "CALL_NO_ANSWER",
  "leadId": "string",
  "campaignId": "string",
  "timestamp": "ISO8601",
  "attemptNumber": "integer"
}
```

**TRIAL_SIGNUP_OFFERED**
```json
{
  "eventType": "TRIAL_SIGNUP_OFFERED",
  "leadId": "string",
  "campaignId": "string",
  "timestamp": "ISO8601",
  "agentAccepted": "boolean"
}
```

**QUALIFICATION_RESULT**
```json
{
  "eventType": "QUALIFICATION_RESULT",
  "leadId": "string",
  "painPoints": ["string"],
  "segment": "string",
  "leadScore": "integer (0-100)",
  "nextAction": "string",
  "timestamp": "ISO8601"
}
```

**UPGRADE_OFFERED**
```json
{
  "eventType": "UPGRADE_OFFERED",
  "leadId": "string",
  "currentPlan": "string",
  "proposedPlan": "string",
  "discount": "percentage",
  "accepted": "boolean",
  "timestamp": "ISO8601"
}
```

## Backend Endpoints

### POST /api/v1/crm/events
**Purpose:** Log call events
**Payload:** Event object (see above)
**Returns:** 200 OK

```bash
curl -X POST http://localhost:8000/api/v1/crm/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "eventType": "CALL_PLACED",
    "leadId": "lead_123",
    "campaignId": "campaign_new_lead"
  }'
```

### GET /api/v1/crm/leads/:leadId
**Purpose:** Fetch lead details
**Returns:** Lead object

### PUT /api/v1/crm/leads/:leadId
**Purpose:** Update lead status
**Payload:** Partial lead object
**Returns:** Updated lead object

### POST /api/v1/crm/cadences
**Purpose:** Enroll lead in cadence
**Payload:** 
```json
{
  "leadId": "string",
  "cadenceId": "string",
  "startDate": "ISO8601"
}
```

## Data Flow

```
Voice Agent → Event Log → /api/v1/crm/events → PostgreSQL
                                            ↓
                              Update Lead Status
                              Trigger Follow-up
                              Update Cadence
                              Log to Analytics
```

## Compliance & Safety

### Opt-Out Handling
- When lead says "STOP" or "REMOVE", immediately:
  1. POST event: `OPTOUT_REQUESTED`
  2. PUT lead: `doNotCall: true, status: 'opted_out'`
  3. Remove from all future cadences
  4. Log timestamp and reason

### Do-Not-Call Registry
- Check lead `doNotCall` flag before any outbound call
- Never attempt call if flag is true
- Update flag if lead opts out mid-call

### Call Recording & Consent
- All calls require explicit consent: "Is it okay if I record this for quality purposes?"
- Only proceed if affirmative
- Store consent in lead record

## Sample Integration Code (Python)

```python
from datetime import datetime
import requests

class VoiceEventLogger:
    def __init__(self, api_url, bearer_token):
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
    
    def log_event(self, event_type, lead_id, **kwargs):
        """Log voice event to backend"""
        payload = {
            "eventType": event_type,
            "leadId": lead_id,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        response = requests.post(
            f"{self.api_url}/api/v1/crm/events",
            json=payload,
            headers=self.headers
        )
        return response.json()
    
    def get_lead(self, lead_id):
        """Fetch lead details"""
        response = requests.get(
            f"{self.api_url}/api/v1/crm/leads/{lead_id}",
            headers=self.headers
        )
        return response.json()
    
    def update_lead_status(self, lead_id, **updates):
        """Update lead in CRM"""
        response = requests.put(
            f"{self.api_url}/api/v1/crm/leads/{lead_id}",
            json=updates,
            headers=self.headers
        )
        return response.json()

# Usage
logger = VoiceEventLogger("http://localhost:8000", "your-token")
logger.log_event("CALL_PLACED", "lead_123", campaignId="campaign_new_lead")
logger.log_event("TRIAL_SIGNUP_OFFERED", "lead_123", agentAccepted=True)
logger.update_lead_status("lead_123", status="trial", lastContactedAt=datetime.now().isoformat())
```

## Summary

| Component | Purpose | Owner |
|-----------|---------|-------|
| Lead Records | Contact data + compliance flags | CRM Backend |
| Events | Voice activity log | Voice Agent → Backend |
| Cadences | Timing + rules for follow-ups | Voice Orchestrator |
| Flows | Call logic + scripts | Voice Agent |
| Endpoints | Backend API for integration | FastAPI |

All voice operations are logged, trackable, and integrated with the sales funnel for analytics and optimization.
