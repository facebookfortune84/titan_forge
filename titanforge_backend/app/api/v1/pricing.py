"""Pricing endpoints for displaying tier information."""

from fastapi import APIRouter
from app.pricing import PricingStructure

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.get("")
async def get_all_pricing():
    """Get all pricing tiers and options."""
    return PricingStructure.get_all_pricing()


@router.get("/tiers")
async def get_pricing_tiers():
    """Get available pricing tiers."""
    return {
        "tiers": [
            {
                "id": "basic",
                "name": "Basic Tier with Concierge",
                "monthly_price_cents": 299900,
                "monthly_price_formatted": "$2,999.00",
                "annual_price_per_month_cents": 249900,
                "annual_price_formatted": "$2,499.00/month (annual billing)",
                "annual_total_cents": 29988 * 100,
                "annual_savings_percent": 17,
            },
            {
                "id": "pro",
                "name": "Professional Tier",
                "monthly_price_cents": 499900,
                "monthly_price_formatted": "$4,999.00",
                "annual_price_per_month_cents": 449900,
                "annual_price_formatted": "$4,499.00/month (annual billing)",
                "annual_total_cents": 53988 * 100,
                "annual_savings_percent": 10,
            }
        ]
    }


@router.get("/basic")
async def get_basic_pricing():
    """Get basic tier details."""
    return PricingStructure.get_basic_tier()


@router.get("/pro")
async def get_pro_pricing():
    """Get pro tier details."""
    return PricingStructure.get_pro_tier()


@router.get("/one-time")
async def get_one_time_services():
    """Get one-time service pricing."""
    pricing = PricingStructure.get_all_pricing()
    return pricing["one_time"]


@router.post("/calculate-discount")
async def calculate_discount(monthly_price_cents: int):
    """Calculate annual discount for given monthly price."""
    savings = PricingStructure.calculate_annual_savings(monthly_price_cents)
    return {
        "monthly_price": monthly_price_cents,
        "monthly_formatted": PricingStructure.format_price(monthly_price_cents),
        "annual_savings": savings,
        "annual_savings_formatted": PricingStructure.format_price(savings),
        "total_annual_cost": (monthly_price_cents * 12) - savings,
        "total_annual_formatted": PricingStructure.format_price((monthly_price_cents * 12) - savings),
    }
