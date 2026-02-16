from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


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


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str  # "subscription" or "one_time_purchase"
    currency: str
    unit_amount: int  # in cents
    interval: Optional[str] = None  # "month", "year"


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

    class Config:
        from_attributes = True


class LeadBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
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
    updated_at: datetime
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BlogPostDetailResponse(BlogPostResponse):
    """Extended response with author info."""
    author: Optional[UserResponse] = None
