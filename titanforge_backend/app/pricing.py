"""Pricing management with new tier structure."""

from enum import Enum
from typing import Dict, List
from decimal import Decimal


class PricingTier(Enum):
    """Available pricing tiers."""
    BASIC = "basic"
    PRO = "pro"
    ONE_TIME = "one_time"


class PricingStructure:
    """Updated pricing structure for sales team."""
    
    TIERS = {
        PricingTier.BASIC: {
            "name": "Basic Tier with Concierge",
            "description": "Complete AI development agency with concierge support",
            "monthly": 299900,  # $2,999.00 in cents
            "yearly": 249900,   # $2,499.00 per month annual billing = $29,988 annual
            "features": [
                "Full AI agent swarm access",
                "Up to 100 tasks per month",
                "Concierge agency support",
                "Priority email support",
                "Custom agent tuning",
                "Lead tracking & CRM",
                "Basic analytics",
            ],
            "annual_savings_percent": 17,  # ~17% savings vs monthly
        },
        PricingTier.PRO: {
            "name": "Professional Tier",
            "description": "Enterprise-grade AI development with advanced features",
            "monthly": 499900,  # $4,999.00 in cents
            "yearly": 449900,   # $4,499.00 per month annual billing = $53,988 annual
            "features": [
                "Unlimited AI agent swarm",
                "Unlimited tasks",
                "Dedicated account manager",
                "24/7 priority support",
                "Custom AI agent development",
                "Advanced lead scoring",
                "White-label capabilities",
                "API access tier 3",
                "Custom integrations",
                "Advanced analytics & reporting",
            ],
            "annual_savings_percent": 10,  # ~10% savings vs monthly
        },
        PricingTier.ONE_TIME: {
            "name": "One-Time Purchases",
            "description": "Custom AI development projects",
            "micro_feature": 499900,      # $4,999
            "api_audit": 249900,           # $2,499
            "performance_optimization": 349900,  # $3,499
            "security_audit": 199900,      # $1,999
            "custom_integration": 599900,  # $5,999
        }
    }

    @staticmethod
    def get_basic_tier() -> Dict:
        """Get basic tier details."""
        return {
            "tier": "basic",
            "monthly_cents": 299900,
            "yearly_cents": 249900,
            "monthly_display": "$2,999/month",
            "yearly_display": "$2,499/month (paid annually)",
            "annual_cost": 29988 * 100,  # in cents
        }

    @staticmethod
    def get_pro_tier() -> Dict:
        """Get pro tier details."""
        return {
            "tier": "pro",
            "monthly_cents": 499900,
            "yearly_cents": 449900,
            "monthly_display": "$4,999/month",
            "yearly_display": "$4,499/month (paid annually)",
            "annual_cost": 53988 * 100,  # in cents
        }

    @staticmethod
    def calculate_annual_savings(monthly_price: int) -> int:
        """Calculate annual savings in cents."""
        # Basic: save 17% = $510/month = $6,120/year
        # Pro: save 10% = $500/month = $6,000/year
        if monthly_price == 299900:  # Basic
            return int(monthly_price * 0.17)
        elif monthly_price == 499900:  # Pro
            return int(monthly_price * 0.10)
        return 0

    @staticmethod
    def format_price(cents: int) -> str:
        """Format cents to USD string."""
        dollars = cents / 100
        return f"${dollars:,.2f}"

    @staticmethod
    def get_all_pricing() -> Dict:
        """Get all pricing information."""
        return {
            "basic": {
                "tier_name": "Basic Tier with Concierge",
                "monthly": {
                    "price_cents": 299900,
                    "price_formatted": "$2,999.00",
                    "billing_cycle": "month"
                },
                "annual": {
                    "price_cents": 249900,
                    "price_formatted": "$2,499.00",
                    "billing_cycle": "month",
                    "total_annual": 29988 * 100,
                    "savings_percent": 17,
                    "savings_cents": 510 * 12 * 100,  # Annual savings
                    "note": "Pay monthly at this rate when billed annually"
                }
            },
            "pro": {
                "tier_name": "Professional Tier",
                "monthly": {
                    "price_cents": 499900,
                    "price_formatted": "$4,999.00",
                    "billing_cycle": "month"
                },
                "annual": {
                    "price_cents": 449900,
                    "price_formatted": "$4,499.00",
                    "billing_cycle": "month",
                    "total_annual": 53988 * 100,
                    "savings_percent": 10,
                    "savings_cents": 500 * 12 * 100,  # Annual savings
                    "note": "Pay monthly at this rate when billed annually"
                }
            },
            "one_time": {
                "micro_feature_dev": {
                    "name": "Micro-Feature Development",
                    "price_cents": 499900,
                    "price_formatted": "$4,999.00"
                },
                "api_audit": {
                    "name": "API Security Audit",
                    "price_cents": 249900,
                    "price_formatted": "$2,499.00"
                },
                "performance_optimization": {
                    "name": "Performance Optimization",
                    "price_cents": 349900,
                    "price_formatted": "$3,499.00"
                },
                "security_audit": {
                    "name": "Security Audit",
                    "price_cents": 199900,
                    "price_formatted": "$1,999.00"
                },
                "custom_integration": {
                    "name": "Custom Integration",
                    "price_cents": 599900,
                    "price_formatted": "$5,999.00"
                }
            }
        }
