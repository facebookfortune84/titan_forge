# Architecture Plan for Monetization & Automation

This document outlines the proposed system architecture to integrate monetization, user management, and enhanced automation within the TitanForge project, based on the audit findings and human inputs.

## 1. User Authentication & Management System

Given the "Build from Scratch" directive, a foundational user management system will be implemented within the existing FastAPI backend and PostgreSQL.

### 1.1. Data Model (`db_models.py` modifications)

A new `User` model will be added to represent platform users.

```python
# In backend/app/db_models.py (Conceptual additions)

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

# Assuming Base is already defined from declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    # For linking GitHub OAuth
    github_id = Column(String, unique=True, index=True, nullable=True)
    # For linking Stripe Customer objects
    stripe_customer_id = Column(String, unique=True, index=True, nullable=True)

    # Relationship to Subscription will be added once Subscription model is defined
    # current_subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=True)
    # subscription = relationship("Subscription", back_populates="user")
```

### 1.2. Authentication Flow

*   **Password Hashing:** Utilize `passlib.context` (e.g., bcrypt) for secure password storage.
*   **JWT for API Access:** Implement JWT (JSON Web Token) generation and verification using `python-jose`.
    *   **Login:** Users authenticate with email/password, receive a JWT.
    *   **Authorization:** JWT token required in `Authorization: Bearer <token>` header for protected endpoints. FastAPI `Depends` will handle token validation.
*   **GitHub OAuth:** Extend existing GitHub OAuth configuration to link `github_id` to `User` records, allowing users to sign up/in via GitHub.

## 2. Subscription & Payment Data Models

New models will be introduced to manage products, subscriptions, and payment intents, forming the backbone of the monetization system.

### 2.1. Data Models (`db_models.py` additions)

```python
# In backend/app/db_models.py (Conceptual additions)

# ... (imports for Column, String, etc. from above)
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB # For storing flexible data like event payloads

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False) # e.g., "Starter AIaaS", "Micro-Feature Dev Package"
    description = Column(String, nullable=True)
    type = Column(String, nullable=False) # e.g., "subscription", "one_time_purchase"
    stripe_price_id = Column(String, unique=True, nullable=True) # Stripe Price ID
    stripe_product_id = Column(String, unique=True, nullable=True) # Stripe Product ID
    currency = Column(String, default="USD", nullable=False)
    unit_amount = Column(Integer, nullable=False) # Price in cents
    interval = Column(String, nullable=True) # "month", "year" for subscriptions, null for one_time
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to subscriptions
    subscriptions = relationship("Subscription", back_populates="product")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    stripe_subscription_id = Column(String, unique=True, nullable=True) # Stripe Subscription ID
    status = Column(String, default="pending", nullable=False) # e.g., "active", "canceled", "past_due"
    current_period_start = Column(DateTime(timezone=True), nullable=True)
    current_period_end = Column(DateTime(timezone=True), nullable=True)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="subscriptions")
    product = relationship("Product", back_populates="subscriptions")

# Add back_populates to User model after Subscription is defined
# User.subscriptions = relationship("Subscription", order_by=Subscription.created_at, back_populates="user")
```

### 2.2. Linking User and Subscription

The `User` model will be updated with a relationship to `Subscription` (one-to-many, as a user can have multiple past subscriptions, though only one *current* active one for the AIaaS platform). A field like `current_subscription_id` could be added to `User` to quickly reference the active AIaaS plan.

```python
# In backend/app/db_models.py (Conceptual modification to User model)

class User(Base):
    # ... (existing fields)
    stripe_customer_id = Column(String, unique=True, index=True, nullable=True)
    current_subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=True)

    subscriptions = relationship("Subscription", back_populates="user")
    current_subscription = relationship("Subscription", foreign_keys=[current_subscription_id])
```

## 3. Agent & Tool Architecture for Monetization Flows

New specialized agents and tools will enhance the automation of monetization, provisioning, and communication.

### 3.1. Proposed New Agents

*   **Billing Agent:**
    *   **Role:** The financial orchestrator. It listens for Stripe webhook events, processes payment confirmations, manages subscription lifecycles (creation, renewal, cancellation), and updates the internal `Subscription` and `User` records in the database. It's responsible for interacting with the Stripe API to fetch customer/subscription details.
    *   **Inputs:** Stripe webhook events (e.g., `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.paid`, `invoice.payment_failed`). Internal requests for payment processing.
    *   **Outputs:** Database updates for `User`, `Product`, `Subscription` models. Triggers `Provisioning Agent` for access changes. Sends notifications via `Notification Agent`.
    *   **Tools it uses:** `Stripe Tool` (new), `Database Tool` (existing/enhanced).
*   **Provisioning Agent:**
    *   **Role:** Manages user entitlements and feature access. Based on `Subscription` status changes or successful one-time `PaymentIntent`s, it activates or deactivates specific features, API limits, agent concurrency, or initiates workflows for productized services.
    *   **Inputs:** `Subscription` status updates from `Billing Agent` (or directly from webhook processing), `PaymentIntent` success notifications.
    *   **Outputs:** Updates user feature flags/limits in the database. Initiates specific agent workflows (e.g., `Orchestrator` to start a development project for a productized service).
    *   **Tools it uses:** `Database Tool`, `Orchestrator Tool` (existing).
*   **Notification Agent:**
    *   **Role:** Centralized communication hub for automated user and internal notifications. Sends transactional emails (welcome, payment success/failure, subscription changes, service updates), and potentially internal alerts (e.g., to Discord for support team).
    *   **Inputs:** Events from `Billing Agent`, `Provisioning Agent`, `Project Agent`, `Analytics Agent` (for reports), etc.
    *   **Outputs:** Sends emails to users, sends messages to internal communication channels (e.g., Discord).
    *   **Tools it uses:** `Email Tool` (existing - needs wrapper for SMTP config), `Discord Tool` (existing).
*   **Analytics Agent:**
    *   **Role:** Collects, processes, aggregates, and reports on key business and system metrics. Tracks user engagement, subscription lifecycle, agent performance, API usage, and revenue.
    *   **Inputs:** Raw event data (user signups, logins, API calls, agent task completions, payment events) from the `Event` table.
    *   **Outputs:** Aggregated metrics (MRR, churn, active users, etc.) stored in a dedicated analytics table or materialized views, which then feed into the dashboard UI. Generates reports for internal stakeholders.
    *   **Tools it uses:** `Database Tool`, potentially a new `Analytics Processing Tool` (for complex data transformations).

### 3.2. Proposed New Tools

*   **Stripe Tool (`swarm/tools/stripe_tool.py`):**
    *   **Purpose:** Encapsulate all interactions with the Stripe API (customer creation, subscription management, checkout session creation, retrieving payment details). Abstracts away direct API calls from agents.
    *   **Interface:** Functions for `create_customer`, `create_checkout_session`, `retrieve_subscription`, `cancel_subscription`, `create_product_and_price` (for initial setup of our `Product` models in Stripe), `handle_webhook_event`.
    *   **Dependencies:** `stripe` Python library (already in `requirements.txt`).
*   **Email Tool (`swarm/tools/email_tool.py` - wrapper for existing SMTP):**
    *   **Purpose:** Provides a simplified interface for agents to send emails, using the existing SMTP configuration from `.env`.
    *   **Interface:** Function for `send_email(to, subject, body, html_body=None)`.
    *   **Dependencies:** Python's `smtplib`, `email.mime.text`.

### 3.3. Existing Agents/Tools Extension

*   **Orchestrator (`swarm/departments/operations/orchestrator.py`):**
    *   Will be extended to receive commands from the `Provisioning Agent` to initiate specific workflows for productized services (e.g., "Start Micro-Feature Development for User X, Task ID Y").
*   **Database Tool (implied):** Agents will require a standardized way to interact with the PostgreSQL database (CRUD operations on `User`, `Product`, `Subscription`, `Event` tables). This could be an explicit `DatabaseTool` or handled via FastAPI dependencies for `Session`.

## 4. Analytics & Reporting Architecture

A simple, effective, and free analytics system will be implemented by logging events to the PostgreSQL database and processing them with the `Analytics Agent`.

### 4.1. Event Data Model (`db_models.py` addition)

```python
# In backend/app/db_models.py (Conceptual addition)

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True) # Optional, for system events
    event_type = Column(String, nullable=False, index=True) # e.g., "user_signup", "subscription_created", "api_call", "agent_task_completed"
    payload = Column(JSONB, nullable=True) # Event-specific data (e.g., {"api_endpoint": "/goals", "status": "success"})
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", backref="events")
```

### 4.2. Analytics Flow

1.  **Event Generation:** Key actions across the system (frontend, backend API, agents) will trigger the creation of records in the `events` table.
2.  **Analytics Agent Processing:** The `Analytics Agent` will periodically (e.g., hourly, daily via `scheduler.py`) query the `events` table, aggregate data, and store summary metrics in a separate table (e.g., `daily_metrics`, `mrr_snapshot`) or materialized views for fast retrieval.
3.  **Dashboard UI:** The frontend (e.g., a new `AnalyticsDashboard.tsx` or an updated `TaskDashboard.tsx`) will fetch these aggregated metrics from dedicated backend API endpoints.

## 5. Summary of Key Data Model Relationships

*   `User` has one-to-many `Subscription`s, and a one-to-one `current_subscription`.
*   `User` has one-to-many `Event`s.
*   `User` can have a `stripe_customer_id` and `github_id`.
*   `Product` has one-to-many `Subscription`s.
*   `Product` is linked to Stripe by `stripe_product_id` and `stripe_price_id`.
*   `Subscription` links `User` to `Product` and tracks Stripe subscription details.
*   `Event` records system activities, optionally linked to a `User`.
