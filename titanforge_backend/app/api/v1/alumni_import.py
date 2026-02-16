"""
DeVry Alumni Pipeline - Lead Import and Outreach
Handles CSV upload for alumni contacts and auto-triggers personalized outreach
"""

import csv
import io
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import re

from ...database import get_db
from ... import db_models
from ...dependencies import get_current_active_user

router = APIRouter(prefix="/leads", tags=["leads"])


class AlumniContact(BaseModel):
    """Represents a single alumni contact from CSV."""
    name: str
    email: EmailStr
    company: Optional[str] = None
    title: Optional[str] = None


class ImportResponse(BaseModel):
    """Response from alumni import."""
    status: str
    imported_count: int
    skipped_count: int
    errors: List[str] = []
    message: str


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@router.post("/import-alumni")
async def import_alumni_contacts(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
) -> ImportResponse:
    """
    Import DeVry alumni contacts from CSV file.
    Expected CSV columns: name, email, company, title
    
    Automatically creates leads and triggers personalized outreach emails.
    """
    
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Only admins can import alumni contacts")
    
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")
    
    try:
        # Read CSV file
        contents = await file.read()
        csv_text = contents.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_text))
        
        imported_count = 0
        skipped_count = 0
        errors = []
        
        # Required columns
        required_columns = {'name', 'email'}
        
        if not csv_reader.fieldnames:
            raise ValueError("CSV file is empty")
        
        csv_columns = set(csv_reader.fieldnames)
        if not required_columns.issubset(csv_columns):
            raise ValueError(f"CSV must contain columns: {', '.join(required_columns)}")
        
        # Process each row
        for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 (header is 1)
            try:
                # Extract and validate data
                name = row.get('name', '').strip()
                email = row.get('email', '').strip()
                company = row.get('company', '').strip()
                title = row.get('title', '').strip()
                
                # Validation
                if not name:
                    errors.append(f"Row {row_num}: Name is required")
                    skipped_count += 1
                    continue
                
                if not email:
                    errors.append(f"Row {row_num}: Email is required")
                    skipped_count += 1
                    continue
                
                if not validate_email(email):
                    errors.append(f"Row {row_num}: Invalid email format: {email}")
                    skipped_count += 1
                    continue
                
                # Check if lead already exists
                existing_lead = db.query(db_models.Lead).filter(
                    db_models.Lead.email == email
                ).first()
                
                if existing_lead:
                    skipped_count += 1
                    continue
                
                # Create new lead
                lead = db_models.Lead(
                    email=email,
                    name=name,
                    company=company if company else "DeVry Alumni",
                    source="devry_alumni_import",
                    status="new",
                    phone=None,
                    message=f"Title: {title}" if title else None,
                )
                
                db.add(lead)
                imported_count += 1
                
                # Trigger agent for personalized outreach email
                # (In production, this would queue an agent task)
                outreach_context = {
                    "contact_name": name,
                    "contact_email": email,
                    "company": company or "DeVry Alumni Network",
                    "title": title,
                    "import_timestamp": datetime.utcnow().isoformat(),
                }
                
                # Log event for agent processing
                event = db_models.Event(
                    user_id=current_user.id,
                    event_type="alumni_outreach_triggered",
                    payload=outreach_context,
                )
                db.add(event)
            
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
                skipped_count += 1
                continue
        
        # Commit all changes
        db.commit()
        
        return ImportResponse(
            status="success" if imported_count > 0 else "partial",
            imported_count=imported_count,
            skipped_count=skipped_count,
            errors=errors if len(errors) > 0 else [],
            message=f"Successfully imported {imported_count} alumni contacts. {skipped_count} skipped."
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")


@router.get("/alumni/status")
async def get_alumni_import_status(
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """Get status of alumni import - count of leads from alumni source."""
    
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Only admins can view import status")
    
    alumni_leads = db.query(db_models.Lead).filter(
        db_models.Lead.source == "devry_alumni_import"
    ).all()
    
    # Calculate metrics
    total = len(alumni_leads)
    new_leads = sum(1 for lead in alumni_leads if lead.status == "new")
    contacted = sum(1 for lead in alumni_leads if lead.status == "contacted")
    converted = sum(1 for lead in alumni_leads if lead.status == "converted")
    
    return {
        "status": "active",
        "total_alumni_leads": total,
        "new_leads": new_leads,
        "contacted": contacted,
        "converted": converted,
        "conversion_rate": f"{(converted / total * 100):.1f}%" if total > 0 else "0%",
        "last_import": max((lead.created_at for lead in alumni_leads), default=None),
    }
