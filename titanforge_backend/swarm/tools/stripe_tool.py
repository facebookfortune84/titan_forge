from typing import Any, Dict, List, Optional

import stripe

from app.core.config import settings


class StripeTool:
    def __init__(self):
        stripe.api_key = settings.STRIPE_API_KEY
        if not stripe.api_key:
            raise ValueError("Stripe API Key is not set in environment variables.")

    def create_customer(self, email: str, user_id: str) -> Dict[str, Any]:
        """Creates a new Stripe customer."""
        try:
            customer = stripe.Customer.create(
                email=email, metadata={"user_id": user_id}
            )
            return customer.to_dict()
        except stripe.error.StripeError as e:
            print(f"Error creating Stripe customer: {e}")
            raise

    def create_checkout_session(
        self,
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
        metadata: Optional[Dict[str, Any]] = None,
        mode: str = "subscription",
    ) -> Dict[str, Any]:
        """Creates a Stripe Checkout Session for subscription or one-time payment."""
        try:
            checkout_session = stripe.checkout.Session.create(
                customer=customer_id,
                line_items=[
                    {"price": price_id, "quantity": 1},
                ],
                mode=mode,
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata,
            )
            return checkout_session.to_dict()
        except stripe.error.StripeError as e:
            print(f"Error creating Stripe Checkout Session: {e}")
            raise

    def retrieve_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Retrieves a Stripe Subscription object."""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return subscription.to_dict()
        except stripe.error.StripeError as e:
            print(f"Error retrieving Stripe Subscription: {e}")
            raise

    def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancels a Stripe Subscription."""
        try:
            canceled_subscription = stripe.Subscription.delete(subscription_id)
            return canceled_subscription.to_dict()
        except stripe.error.StripeError as e:
            print(f"Error canceling Stripe Subscription: {e}")
            raise

    def construct_webhook_event(self, payload: bytes, sig_header: str) -> stripe.Event:
        """Constructs a Stripe Event from a webhook payload."""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            # Invalid payload
            print(f"Error constructing webhook event: Invalid payload: {e}")
            raise
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            print(f"Error constructing webhook event: Invalid signature: {e}")
            raise

    def get_all_products_and_prices(self) -> List[Dict[str, Any]]:
        """Retrieves all active Stripe Products and their Prices."""
        products_with_prices = []
        try:
            products = stripe.Product.list(active=True, expand=["default_price"])
            for product in products.data:
                if product.default_price:
                    products_with_prices.append(
                        {
                            "product_id": product.id,
                            "product_name": product.name,
                            "price_id": product.default_price.id,
                            "unit_amount": product.default_price.unit_amount,
                            "currency": product.default_price.currency,
                            "interval": (
                                product.default_price.recurring.interval
                                if product.default_price.recurring
                                else None
                            ),
                            "type": (
                                "subscription"
                                if product.default_price.recurring
                                else "one_time_purchase"
                            ),
                        }
                    )
            return products_with_prices
        except stripe.error.StripeError as e:
            print(f"Error fetching Stripe products and prices: {e}")
            raise

    def create_product_and_price(
        self,
        name: str,
        unit_amount: int,  # in cents
        currency: str,
        interval: Optional[str] = None,  # "month", "year" etc. for recurring
        interval_count: Optional[int] = 1,
        product_description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a Stripe Product and an associated Price."""
        try:
            product = stripe.Product.create(
                name=name,
                description=product_description,
                type="service",  # Or "good" depending on the offering
            )
            price_data = {
                "unit_amount": unit_amount,
                "currency": currency,
                "product": product.id,
            }
            if interval:
                price_data["recurring"] = {
                    "interval": interval,
                    "interval_count": interval_count,
                }

            price = stripe.Price.create(**price_data)
            return {"product": product.to_dict(), "price": price.to_dict()}
        except stripe.error.StripeError as e:
            print(f"Error creating Stripe product and price: {e}")
            raise
