from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

# ============================================================
# Auth Schemas
# ============================================================

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    github_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class AuthTokens(BaseModel):
    access_token: str
    token_type: str

# ============================================================
# Task Schemas
# ============================================================

class Task(BaseModel):
    id: str
    goal: str
    status: str
    created_at: str
    updated_at: str
    user_id: str
    result: Optional[str] = None
    error: Optional[str] = None

# ============================================================
# Scheduler Schemas
# ============================================================

class ScheduledJob(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    schedule: str
    next_run_time: str
    last_run_time: Optional[str] = None
    is_active: bool
    status: str

# ============================================================
# Agent Schemas
# ============================================================

class Agent(BaseModel):
    agent_id: str
    role: str
    department: str
    model_name: Optional[str] = None
    is_active: bool
    status: Optional[str] = None
    description: Optional[str] = None

class Message(BaseModel):
    sender_id: str
    recipient_id: str
    content: str
    timestamp: str
    message_type: Optional[str] = None

# ============================================================
# Graph Schemas
# ============================================================

class GraphNode(BaseModel):
    id: str
    name: str
    type: str
    status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class GraphLink(BaseModel):
    source: str
    target: str
    relationship: str
    weight: Optional[float] = None

class GraphData(BaseModel):
    nodes: List[GraphNode]
    links: List[GraphLink]

# ============================================================
# Product & Payment Schemas
# ============================================================

class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    currency: str
    stripe_product_id: str
    stripe_price_id: str
    features: List[str]
    active: bool

class CheckoutSession(BaseModel):
    session_id: str
    url: str
    expires_at: str

class Transaction(BaseModel):
    id: str
    user_id: str
    amount: float
    currency: str
    status: str
    product_id: Optional[str] = None
    created_at: str
    description: Optional[str] = None

class IncomeReport(BaseModel):
    total_revenue: float
    total_transactions: int
    currency: str
    period: Dict[str, str]
    breakdown: Optional[Dict[str, float]] = None

# ============================================================
# Analytics Schemas
# ============================================================

class AnalyticsSummary(BaseModel):
    total_users: int
    new_signups_this_month: int
    active_subscriptions: int
    mrr_estimate: float
    churn_rate: float
    retention_rate: float
    avg_revenue_per_user: float

# ============================================================
# File & Swarm Schemas
# ============================================================

class FileContent(BaseModel):
    path: str
    content: str
    size: Optional[int] = None
    type: Optional[str] = None

class DepartmentStatus(BaseModel):
    name: str
    agent_count: int
    active_agents: int
    status: str

class SwarmStatus(BaseModel):
    total_agents: int
    active_agents: int
    departments: List[DepartmentStatus]
    system_health: str
    uptime_seconds: int

# ============================================================
# API Schemas
# ============================================================

class ApiError(BaseModel):
    detail: str
    status_code: int
    error_type: Optional[str] = None

template_T = "T"

class PaginatedResponse(BaseModel):
    items: List[template_T]
    total: int
    page: int
    page_size: int
    total_pages: int

# ============================================================
# Lead Schemas
# ============================================================

class LeadBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    message: Optional[str] = None

class LeadCreate(LeadBase):
    source: Optional[str] = "landing_page"

class LeadResponse(LeadBase):
    id: UUID
    source: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================================
# Blog Schemas
# ============================================================

class BlogPostBase(BaseModel):
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    featured_image_url: Optional[str] = None
    tags: Optional[list] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None

class BlogPostCreate(BlogPostBase):
    author_id: UUID
    published: Optional[bool] = False

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    featured_image_url: Optional[str] = None
    tags: Optional[list] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    published: Optional[bool] = None

class BlogPostResponse(BlogPostBase):
    id: UUID
    author_id: UUID
    published: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BlogPostDetailResponse(BlogPostResponse):
    """Extended response with author info."""
    author: Optional[UserResponse] = None

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    currency: str
    unit_amount: int
    interval: Optional[str] = None

class ProductCreate(ProductBase):
    stripe_price_id: str
    stripe_product_id: str

class ProductResponse(ProductBase):
    id: UUID
    stripe_price_id: Optional[str] = None
    stripe_product_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    price: float = Field(..., alias='price')

    class Config:
        from_attributes = True
        #This is a Pydantic V2 feature, if it fails, I will use a different approach
        @classmethod
        def from_orm(cls, obj):
            obj.price = obj.unit_amount / 100
            return super().from_orm(obj)
