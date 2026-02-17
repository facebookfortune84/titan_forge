"""Pricing endpoints for displaying tier information."""

from fastapi import APIRouter

router = APIRouter(prefix="/pricing", tags=["pricing"])

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
