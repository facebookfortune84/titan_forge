ACTION PROPOSAL [33]: Create ANALYTICS_SETUP.md documentation.

Rationale: This document will provide guidance on the analytics setup, including how metrics are collected, processed, and displayed, assisting with system understanding and future extensions.

---
# Analytics Setup Documentation

This document describes the analytics infrastructure implemented in TitanForge AI, covering event collection, processing, and dashboard visualization.

## 1. Event Collection

### 1.1. Backend Event Recording
Key user and system actions are recorded as `Event` entries in the PostgreSQL database. This is handled by the `AnalyticsAgent` which receives messages from various parts of the backend.

*   **Mechanism:** The `send_agent_message` utility in `backend/app/main.py` is used to send event data to the `analytics_agent`'s Redis queue.
*   **Trigger Points:**
    *   **User Signup:** When a new user registers (`/register` endpoint in `main.py`).
    *   **Goal Submission:** When a user submits a goal (`/goals` endpoint in `main.py`).
    *   **Future Events:** Other events (e.g., `subscription_created`, `payment_succeeded`, `agent_task_completed`, `api_call`) will be recorded by relevant agents (e.g., `BillingAgent`, `ProvisioningAgent`) by sending messages to the `analytics_agent`.

### 1.2. `Event` Data Model
Events are stored in the `events` table (defined in `backend/app/db_models.py`):
```python
class Event(Base):
    __tablename__ = "events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    event_type = Column(String, nullable=False, index=True)
    payload = Column(JSONB, nullable=True) # JSONB for flexible event-specific data
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
```

## 2. Event Processing & Metric Aggregation

### 2.1. `AnalyticsAgent` Role
The `AnalyticsAgent` (located in `swarm/departments/data_intelligence/analytics_agent.py`) is responsible for:
*   Ingesting raw event data from its Redis queue (triggered by `send_agent_message`).
*   Recording these events into the `events` table.
*   Aggregating raw event data into summarized metrics.

### 2.2. Scheduled Aggregation
A daily scheduled task triggers the `AnalyticsAgent` to perform metric aggregation.

*   **Scheduler Job:** A `cron` job named `daily_analytics_aggregation` is configured in `backend/app/scheduler.py` to run daily (e.g., at 2 AM UTC).
*   **Process:** This job sends a message to the `analytics_agent`'s Redis queue with an `action: "aggregate_daily_metrics"`. The `AnalyticsAgent` then queries the `events` table, calculates metrics (e.g., new signups, active subscriptions), and can optionally store these in a separate `aggregated_metrics` table for faster dashboard loading (currently, it calculates on-the-fly for the dashboard).

## 3. Dashboard Visualization

### 3.1. Backend API Endpoint
Aggregated analytics data is exposed via a secured FastAPI endpoint.

*   **Endpoint:** `/analytics/summary` in `backend/app/main.py`.
*   **Security:** This endpoint is protected and only accessible by users with `is_superuser = True`.
*   **Metrics Provided:**
    *   `total_users`: Total number of registered users.
    *   `total_signups`: Total number of `user_signup` events (lifetime).
    *   `active_subscriptions`: Count of currently active subscriptions.
    *   `mrr_estimate_usd`: Estimated Monthly Recurring Revenue (calculated by summing monthly equivalent of all active subscriptions).

### 3.2. Frontend Dashboard
The `AnalyticsDashboard` React component displays these metrics in a user-friendly format.

*   **Component:** `frontend/src/AnalyticsDashboard.tsx`.
*   **Access:** Navigable via `/analytics` route. Access is restricted to superusers.
*   **Data Fetching:** The component fetches data from the `/analytics/summary` endpoint upon loading, passing the user's authentication token.

## 4. Future Enhancements

*   **Dedicated Aggregated Metrics Table:** For large datasets, pre-aggregating metrics into a dedicated table would improve dashboard performance significantly.
*   **More Granular Metrics:** Implement tracking for API usage, agent task completion rates, feature adoption, churn rate, conversion funnels (trial-to-paid, lead-to-customer).
*   **Time-Series Data:** Implement charts and graphs to visualize trends over time (daily, weekly, monthly).
*   **Admin UI for Events:** A UI to view raw `Event` data for debugging and detailed analysis.
*   **External Analytics Integration:** Option to integrate with third-party, open-source analytics platforms (e.g., PostHog, Matomo) for richer insights.
