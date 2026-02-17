import uuid

from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


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
    github_id = Column(String, unique=True, index=True, nullable=True)
    stripe_customer_id = Column(String, unique=True, index=True, nullable=True)
    current_subscription_id = Column(
        UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=True
    )

    subscriptions = relationship(
        "Subscription", back_populates="user", foreign_keys="[Subscription.user_id]"
    )
    current_subscription = relationship(
        "Subscription", foreign_keys=[current_subscription_id], post_update=True
    )
    events = relationship("Event", back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(
        String, nullable=False
    )  # e.g., "Starter AIaaS", "Micro-Feature Dev Package"
    description = Column(String, nullable=True)
    type = Column(String, nullable=False)  # e.g., "subscription", "one_time_purchase"
    stripe_price_id = Column(String, unique=True, nullable=True)  # Stripe Price ID
    stripe_product_id = Column(String, unique=True, nullable=True)  # Stripe Product ID
    currency = Column(String, default="USD", nullable=False)
    unit_amount = Column(Integer, nullable=False)  # Price in cents
    interval = Column(
        String, nullable=True
    )  # "month", "year" for subscriptions, null for one_time
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    subscriptions = relationship("Subscription", back_populates="product")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    stripe_subscription_id = Column(
        String, unique=True, nullable=True
    )  # Stripe Subscription ID
    status = Column(
        String, default="pending", nullable=False
    )  # e.g., "active", "canceled", "past_due"
    current_period_start = Column(DateTime(timezone=True), nullable=True)
    current_period_end = Column(DateTime(timezone=True), nullable=True)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="subscriptions", foreign_keys=[user_id])
    product = relationship("Product", back_populates="subscriptions")


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )  # Optional, for system events
    event_type = Column(
        String, nullable=False, index=True
    )  # e.g., "user_signup", "subscription_created", "api_call", "agent_task_completed"
    payload = Column(
        JSON, nullable=True
    )  # Event-specific data (e.g., {"api_endpoint": "/goals", "status": "success"})
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="events")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String, index=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime)
    history = Column(JSON)



class StripeTransaction(Base):
    __tablename__ = "stripe_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stripe_event_id = Column(String, unique=True, index=True, nullable=False)
    payment_intent_id = Column(String, index=True, nullable=True)
    customer_id = Column(String, index=True, nullable=True)
    amount = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    raw_event = Column(JSON, nullable=False)


class Lead(Base):
    """Represents a lead captured from landing page or other sources."""
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    company = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    message = Column(String, nullable=True)
    source = Column(String, default="landing_page", nullable=False)  # where lead came from
    status = Column(String, default="new", nullable=False)  # new, contacted, converted, lost
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    converted_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # if converted to user

    converted_user = relationship("User", foreign_keys=[converted_user_id])


class BlogPost(Base):
    """Represents a blog post for SEO and content marketing."""
    __tablename__ = "blog_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    content = Column(String, nullable=False)  # Markdown content
    excerpt = Column(String(500), nullable=True)
    featured_image_url = Column(String, nullable=True)
    tags = Column(JSON, default=list, nullable=False)  # e.g., ["ai", "saas", "automation"]
    meta_title = Column(String(255), nullable=True)  # For SEO
    meta_description = Column(String(500), nullable=True)  # For SEO
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    published = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)

    author = relationship("User", foreign_keys=[author_id])
