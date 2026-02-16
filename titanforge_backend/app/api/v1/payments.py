from typing import List
import redis
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from swarm.tools.stripe_tool import StripeTool

from ... import db_models, schemas
from ...database import get_db
from ...dependencies import get_current_active_user, send_agent_message
from ...redis_client import get_redis

router = APIRouter()
stripe_tool = StripeTool()


class CreateCheckoutSessionRequest(BaseModel):
    product_id: str  # Our internal product UUID
    success_url: str
    cancel_url: str


@router.post("/create-checkout-session")
async def create_checkout_session(
    request: CreateCheckoutSessionRequest,
    db: Session = Depends(get_db),
    r: redis.Redis = Depends(get_redis),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """
    Creates a Stripe Checkout Session for a given product.
    """
    db_product = (
        db.query(db_models.Product)
        .filter(db_models.Product.id == request.product_id)
        .first()
    )
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )

    if not db_product.stripe_price_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stripe Price ID not configured for this product.",
        )

    # Ensure user has a Stripe customer ID, create if not
    if not current_user.stripe_customer_id:
        try:
            customer = stripe_tool.create_customer(
                email=current_user.email, user_id=str(current_user.id)
            )
            current_user.stripe_customer_id = customer["id"]
            db.add(current_user)
            db.commit()
            db.refresh(current_user)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create Stripe customer: {e}",
            )

    try:
        checkout_session = stripe_tool.create_checkout_session(
            customer_id=current_user.stripe_customer_id,
            price_id=db_product.stripe_price_id,
            success_url=request.success_url,
            cancel_url=request.cancel_url,
            metadata={
                "user_id": str(current_user.id),
                "product_id": str(db_product.id),
                "product_type": db_product.type,
            },
            mode="subscription" if db_product.type == "subscription" else "payment",
        )
        return {"id": checkout_session["id"], "url": checkout_session["url"]}
    except Exception as e:
        # Optionally send internal error notification
        send_agent_message(
            recipient_id="notification_agent",
            sender_id="payments_api",
            message_content={
                "action": "process_notification_request",
                "notification_type": "internal_error",
                "data": {
                    "error_message": f"Failed to create Stripe checkout session for user {current_user.email}, product {db_product.name}: {e}"
                },
            },
            r=r,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create checkout session: {e}",
        )


@router.get("/products", response_model=List[schemas.ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    """
    Retrieve a list of all active products (subscriptions and one-time purchases).
    """
    products = (
        db.query(db_models.Product).filter(db_models.Product.is_active is True).all()
    )
    return products


# You might want to add additional endpoints here, e.g., for managing subscriptions
# @router.post("/manage-subscription")
# async def manage_subscription(...):
#     pass
