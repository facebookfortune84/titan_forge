from datetime import datetime

import stripe

from app import crud, db_models
from app.core.config import settings
from app.database import get_db_session_from_agent
from swarm.agents.base_agent import BaseAgent
from swarm.tools.stripe_tool import StripeTool


class BillingAgent(BaseAgent):
    def __init__(self, model_name: str = settings.LLM_MODEL_NAME):
        super().__init__(
            role="Manages all financial transactions, subscriptions, and billing inquiries.",
            department="finance",
            model_name=model_name,
        )
        self.stripe_tool = StripeTool()

    def execute_task(self, task_description: str) -> str:
        print(f"BillingAgent received task: {task_description}")
        return "Task received."

    def handle_webhook_event(self, event_payload: bytes, signature: str):
        """
        Processes an incoming Stripe webhook event.
        """
        try:
            event = self.stripe_tool.construct_webhook_event(event_payload, signature)
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            print(f"Webhook Error: {e}")
            return {"status": "error", "message": str(e)}

        db = next(get_db_session_from_agent())  # Get a DB session

        try:
            # Store raw event for auditing
            stripe_transaction = db_models.StripeTransaction(
                stripe_event_id=event.id,
                payment_intent_id=(
                    event.data.object.id if hasattr(event.data.object, "id") else None
                ),
                customer_id=(
                    event.data.object.customer
                    if hasattr(event.data.object, "customer")
                    else None
                ),
                amount="N/A",  # Will populate more specifically per event type
                currency="N/A",  # Will populate more specifically per event type
                status="received",
                created_at=datetime.fromtimestamp(event.created),
                raw_event=event.data.object,
            )
            db.add(stripe_transaction)
            db.commit()
            db.refresh(stripe_transaction)

            event_type = event.type
            data_object = event.data.object

            print(f"Processing Stripe event: {event_type}")

            if event_type == "checkout.session.completed":
                customer_id = data_object.customer
                subscription_id = data_object.subscription
                user_id = data_object.metadata.get(
                    "user_id"
                )  # Assuming user_id is passed in metadata
                product_id = data_object.metadata.get(
                    "product_id"
                )  # Assuming product_id is passed in metadata

                if user_id and customer_id:
                    user = crud.get_user(db, user_id)
                    if user and not user.stripe_customer_id:
                        user.stripe_customer_id = customer_id
                        db.add(user)
                        # Optionally, link product if it's a one-time purchase
                    if subscription_id and product_id:
                        # Create or update subscription in DB
                        sub = db_models.Subscription(
                            user_id=user_id,
                            product_id=product_id,
                            stripe_subscription_id=subscription_id,
                            status="active",  # Should be active for completed session
                            current_period_start=datetime.fromtimestamp(
                                data_object.created
                            ),  # Placeholder, actual start comes from subscription obj
                            current_period_end=datetime.fromtimestamp(
                                data_object.expires_at
                            ),  # Placeholder
                        )
                        db.add(sub)
                        db.flush()  # Flush to get subscription ID
                        if user:
                            user.current_subscription_id = sub.id
                            db.add(user)

                    db.commit()
                    # Trigger provisioning agent here
                    # self.send_message("provisioning_agent", "subscription_activated", {"user_id": user_id, "subscription_id": str(sub.id)})

            elif (
                event_type == "customer.subscription.created"
                or event_type == "customer.subscription.updated"
            ):
                subscription_id = data_object.id
                status = data_object.status
                user_id = data_object.metadata.get(
                    "user_id"
                )  # Assuming user_id is stored in subscription metadata
                customer_id = data_object.customer

                db_subscription = (
                    db.query(db_models.Subscription)
                    .filter(
                        db_models.Subscription.stripe_subscription_id == subscription_id
                    )
                    .first()
                )
                if not db_subscription:
                    # This might happen if checkout.session.completed didn't create it, or direct subscription creation
                    # Need to retrieve product_id from Stripe product linked to this subscription
                    print(
                        f"Subscription {subscription_id} not found in DB. Attempting to create."
                    )
                    items = data_object.items.data
                    if items:
                        price_id = items[0].price.id
                        db_product = (
                            db.query(db_models.Product)
                            .filter(db_models.Product.stripe_price_id == price_id)
                            .first()
                        )
                        if (
                            db_product and user_id
                        ):  # user_id needs to be in metadata on subscription
                            db_subscription = db_models.Subscription(
                                user_id=user_id,
                                product_id=db_product.id,
                                stripe_subscription_id=subscription_id,
                                status=status,
                                current_period_start=datetime.fromtimestamp(
                                    data_object.current_period_start
                                ),
                                current_period_end=datetime.fromtimestamp(
                                    data_object.current_period_end
                                ),
                                cancel_at_period_end=data_object.cancel_at_period_end,
                            )
                            db.add(db_subscription)
                            db.flush()
                            db_user = crud.get_user(db, user_id)
                            if db_user:
                                db_user.current_subscription_id = db_subscription.id
                                db.add(db_user)
                            db.commit()
                        else:
                            print(
                                f"Could not find product or user for new subscription {subscription_id}"
                            )
                            db.rollback()
                            return {
                                "status": "warning",
                                "message": f"Subscription {subscription_id} not fully processed due to missing product/user.",
                            }
                else:
                    db_subscription.status = status
                    db_subscription.current_period_start = datetime.fromtimestamp(
                        data_object.current_period_start
                    )
                    db_subscription.current_period_end = datetime.fromtimestamp(
                        data_object.current_period_end
                    )
                    db_subscription.cancel_at_period_end = (
                        data_object.cancel_at_period_end
                    )
                    db.add(db_subscription)
                    db.commit()
                # Trigger provisioning agent here
                # self.send_message("provisioning_agent", "subscription_updated", {"user_id": user_id, "subscription_id": db_subscription.id, "status": status})

            elif event_type == "customer.subscription.deleted":
                subscription_id = data_object.id
                db_subscription = (
                    db.query(db_models.Subscription)
                    .filter(
                        db_models.Subscription.stripe_subscription_id == subscription_id
                    )
                    .first()
                )
                if db_subscription:
                    db_subscription.status = "canceled"
                    db.add(db_subscription)
                    # Also remove from user's current_subscription_id if it matches
                    user = crud.get_user(db, db_subscription.user_id)
                    if user and user.current_subscription_id == db_subscription.id:
                        user.current_subscription_id = None
                        db.add(user)
                    db.commit()
                    # Trigger provisioning agent here
                    # self.send_message("provisioning_agent", "subscription_canceled", {"user_id": db_subscription.user_id, "subscription_id": db_subscription.id})

            elif event_type == "invoice.payment_succeeded":
                payment_intent_id = data_object.payment_intent
                amount = data_object.amount_paid
                currency = data_object.currency
                customer_id = data_object.customer

                # Update StripeTransaction with more details
                db_transaction = (
                    db.query(db_models.StripeTransaction)
                    .filter(
                        db_models.StripeTransaction.payment_intent_id
                        == payment_intent_id
                    )
                    .first()
                )
                if db_transaction:
                    db_transaction.status = "succeeded"
                    db_transaction.amount = str(amount)  # store in cents as string
                    db_transaction.currency = currency
                    db.add(db_transaction)
                else:
                    # Create if not already stored by checkout.session.completed
                    stripe_transaction = db_models.StripeTransaction(
                        stripe_event_id=event.id,
                        payment_intent_id=payment_intent_id,
                        customer_id=customer_id,
                        amount=str(amount),
                        currency=currency,
                        status="succeeded",
                        created_at=datetime.fromtimestamp(event.created),
                        raw_event=data_object,
                    )
                    db.add(stripe_transaction)
                db.commit()
                # Trigger notification agent for payment confirmation
                # self.send_message("notification_agent", "payment_succeeded", {"user_id": user_id_from_customer, "amount": amount, "currency": currency})

            elif event_type == "invoice.payment_failed":
                payment_intent_id = data_object.payment_intent
                customer_id = data_object.customer

                db_transaction = (
                    db.query(db_models.StripeTransaction)
                    .filter(
                        db_models.StripeTransaction.payment_intent_id
                        == payment_intent_id
                    )
                    .first()
                )
                if db_transaction:
                    db_transaction.status = "failed"
                    db.add(db_transaction)
                else:
                    stripe_transaction = db_models.StripeTransaction(
                        stripe_event_id=event.id,
                        payment_intent_id=payment_intent_id,
                        customer_id=customer_id,
                        amount="N/A",  # Amount may not be available for failed payments
                        currency="N/A",
                        status="failed",
                        created_at=datetime.fromtimestamp(event.created),
                        raw_event=data_object,
                    )
                    db.add(stripe_transaction)
                db.commit()
                # Trigger notification agent for payment failure
                # self.send_message("notification_agent", "payment_failed", {"user_id": user_id_from_customer})

            else:
                print(f"Unhandled event type: {event_type}")

            db.close()
            return {"status": "success", "message": f"Event {event_type} processed."}

        except Exception as e:
            db.rollback()
            db.close()
            print(f"Error processing Stripe webhook event {event.type}: {e}")
            return {"status": "error", "message": f"Error processing event: {e}"}
