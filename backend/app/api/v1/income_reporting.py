from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ... import db_models
from ...database import get_db

router = APIRouter()


@router.get("/income/transactions", response_model=List[Dict[str, Any]])
async def get_all_transactions(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    """
    Retrieves all recorded Stripe transactions.
    """
    transactions = db.query(db_models.StripeTransaction).offset(skip).limit(limit).all()
    return [
        {
            "id": str(t.id),
            "stripe_event_id": t.stripe_event_id,
            "payment_intent_id": t.payment_intent_id,
            "customer_id": t.customer_id,
            "amount": t.amount,
            "currency": t.currency,
            "status": t.status,
            "created_at": t.created_at.isoformat(),
            # "raw_event": t.raw_event # Exclude raw event for brevity in list, can add specific endpoint for detail
        }
        for t in transactions
    ]


@router.get("/income/summary")
async def get_income_summary(
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(
        None, description="Start date for income summary (ISO 8601 format)"
    ),
    end_date: Optional[datetime] = Query(
        None, description="End date for income summary (ISO 8601 format)"
    ),
):
    """
    Provides a summary of income, optionally filtered by date range.
    Amounts are summed per currency.
    """
    query = db.query(db_models.StripeTransaction).filter(
        db_models.StripeTransaction.status == "completed"
    )

    if start_date:
        query = query.filter(db_models.StripeTransaction.created_at >= start_date)
    if end_date:
        # Ensure end_date includes the entire day
        end_date_with_time = (
            end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            if end_date
            else None
        )
        query = query.filter(
            db_models.StripeTransaction.created_at <= end_date_with_time
        )

    transactions = query.all()

    total_income_by_currency = {}
    for t in transactions:
        try:
            amount = float(t.amount)
            if t.currency not in total_income_by_currency:
                total_income_by_currency[t.currency] = 0.0
            total_income_by_currency[t.currency] += amount
        except ValueError:
            print(
                f"Warning: Could not convert amount '{t.amount}' to float for transaction {t.id}"
            )

    return {
        "total_transactions": len(transactions),
        "total_income_by_currency": total_income_by_currency,
        "start_date": start_date.isoformat() if start_date else "beginning",
        "end_date": end_date.isoformat() if end_date else "now",
    }


@router.get("/income/transaction/{transaction_id}", response_model=Dict[str, Any])
async def get_transaction_details(transaction_id: str, db: Session = Depends(get_db)):
    """
    Retrieves detailed information for a specific transaction.
    """
    transaction = (
        db.query(db_models.StripeTransaction)
        .filter(db_models.StripeTransaction.id == transaction_id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found.")

    return {
        "id": str(transaction.id),
        "stripe_event_id": transaction.stripe_event_id,
        "payment_intent_id": transaction.payment_intent_id,
        "customer_id": transaction.customer_id,
        "amount": transaction.amount,
        "currency": transaction.currency,
        "status": transaction.status,
        "created_at": transaction.created_at.isoformat(),
        "raw_event": transaction.raw_event,
    }
