from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ... import db_models
from ...database import get_db
from ...dependencies import get_current_active_user

router = APIRouter()

@router.get("/summary")
async def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view analytics.",
        )

    total_users = db.query(db_models.User).count()
    total_signups = (
        db.query(db_models.Event)
        .filter(db_models.Event.event_type == "user_signup")
        .count()
    )
    active_subscriptions = (
        db.query(db_models.Subscription)
        .filter(db_models.Subscription.status == "active")
        .count()
    )

    mrr_estimate = 0
    active_subs = (
        db.query(db_models.Subscription)
        .filter(db_models.Subscription.status == "active")
        .all()
    )
    for sub in active_subs:
        product = (
            db.query(db_models.Product)
            .filter(db_models.Product.id == sub.product_id)
            .first()
        )
        if product and product.type == "subscription":
            if product.interval == "month":
                mrr_estimate += product.unit_amount
            elif product.interval == "year":
                mrr_estimate += product.unit_amount / 12

    mrr_estimate_dollars = mrr_estimate / 100

    return {
        "total_users": total_users,
        "total_signups": total_signups,
        "active_subscriptions": active_subscriptions,
        "mrr_estimate_usd": round(mrr_estimate_dollars, 2),
    }
