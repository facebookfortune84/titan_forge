from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from email_validator import validate_email, EmailNotValidError

from ... import db_models, schemas
from ...database import get_db
from ...dependencies import send_agent_message
import redis
from ...redis_client import get_redis

router = APIRouter()


@router.post("/leads", response_model=schemas.LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db),
    r: redis.Redis = Depends(get_redis),
):
    """
    Capture a lead from the landing page or other sources.
    
    This endpoint stores lead information and triggers follow-up actions
    (email notifications, analytics recording, etc.)
    """
    
    # Validate email format
    try:
        valid = validate_email(lead.email)
        email = valid.email
    except EmailNotValidError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid email: {str(e)}"
        )
    
    # Check if lead already exists
    existing_lead = db.query(db_models.Lead).filter(
        db_models.Lead.email == email
    ).first()
    
    if existing_lead:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email has already been captured"
        )
    
    # Create new lead
    db_lead = db_models.Lead(
        email=email,
        name=lead.name,
        company=lead.company,
        phone=lead.phone,
        message=lead.message,
        source=lead.source or "landing_page",
        status="new"
    )
    
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    # Send lead_captured event to analytics agent
    send_agent_message(
        recipient_id="analytics_agent",
        sender_id="mcp",
        message_content={
            "action": "record_event",
            "event_type": "lead_captured",
            "payload": {
                "lead_id": str(db_lead.id),
                "email": db_lead.email,
                "source": db_lead.source,
                "company": db_lead.company
            },
        },
        r=r,
    )
    
    # Send welcome message to notification agent
    send_agent_message(
        recipient_id="notification_agent",
        sender_id="mcp",
        message_content={
            "action": "process_notification_request",
            "notification_type": "lead_welcome",
            "data": {
                "lead_email": db_lead.email,
                "lead_name": db_lead.name or db_lead.email.split("@")[0],
            },
        },
        r=r,
    )
    
    return db_lead


@router.get("/leads", response_model=List[schemas.LeadResponse])
async def list_leads(
    db: Session = Depends(get_db),
):
    """
    Get all captured leads (public endpoint for now, but should require admin auth).
    """
    leads = db.query(db_models.Lead).order_by(db_models.Lead.created_at.desc()).all()
    return leads


@router.get("/leads/{lead_id}", response_model=schemas.LeadResponse)
async def get_lead(
    lead_id: str,
    db: Session = Depends(get_db),
):
    """
    Get a specific lead by ID.
    """
    lead = db.query(db_models.Lead).filter(db_models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    return lead
