"""
Stripe Products Setup Script
Creates TitanForge pricing tiers in Stripe if they don't exist
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv("F:/TitanForge/titanforge_backend/.env")

try:
    import stripe
except ImportError:
    print("Installing stripe package...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "stripe"])
    import stripe

# Initialize Stripe
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
if not STRIPE_API_KEY:
    print("ERROR: STRIPE_API_KEY not found in environment variables")
    sys.exit(1)

stripe.api_key = STRIPE_API_KEY


def check_and_create_products():
    """Check if products exist, create if not."""
    
    # Define products
    products_config = [
        {
            "name": "TitanForge Basic",
            "description": "Basic automation package - $2,999/month",
            "prices": [
                {"amount": 299900, "currency": "usd", "recurring": {"interval": "month"}, "nickname": "Basic Monthly"},
                {"amount": 2999900, "currency": "usd", "recurring": {"interval": "year"}, "nickname": "Basic Annual"},
            ]
        },
        {
            "name": "TitanForge Pro",
            "description": "Pro automation package - $4,999/month",
            "prices": [
                {"amount": 499900, "currency": "usd", "recurring": {"interval": "month"}, "nickname": "Pro Monthly"},
                {"amount": 4499900, "currency": "usd", "recurring": {"interval": "year"}, "nickname": "Pro Annual"},
            ]
        }
    ]
    
    try:
        # List existing products
        existing_products = stripe.Product.list(limit=100)
        existing_names = {p.name for p in existing_products.data}
        
        print("Existing Stripe Products:")
        for product in existing_products.data:
            print(f"  - {product.name} (ID: {product.id})")
        print()
        
        # Create products if they don't exist
        created_products = {}
        for config in products_config:
            if config["name"] not in existing_names:
                print(f"Creating product: {config['name']}...")
                product = stripe.Product.create(
                    name=config["name"],
                    description=config["description"],
                    type="service",
                )
                created_products[config["name"]] = product
                print(f"  ✓ Created: {config['name']} (ID: {product.id})")
                
                # Create prices for the product
                for price_config in config["prices"]:
                    price = stripe.Price.create(
                        product=product.id,
                        unit_amount=price_config["amount"],
                        currency=price_config["currency"],
                        recurring=price_config["recurring"],
                        nickname=price_config["nickname"],
                    )
                    print(f"    ✓ Price created: {price_config['nickname']} (ID: {price.id})")
            else:
                print(f"Product already exists: {config['name']}")
                # List prices for existing product
                products_by_name = {p.name: p for p in existing_products.data}
                product = products_by_name[config["name"]]
                prices = stripe.Price.list(product=product.id, limit=10)
                for price in prices.data:
                    print(f"    - {price.nickname}: ${price.unit_amount/100:.2f} {price.recurring['interval'] if price.recurring else 'one-time'}")
        
        print("\n✅ Stripe products verification complete!")
        return True
        
    except stripe.error.StripeError as e:
        print(f"❌ Stripe API Error: {e.message}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    success = check_and_create_products()
    sys.exit(0 if success else 1)
