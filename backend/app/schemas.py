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
