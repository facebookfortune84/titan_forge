from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ... import crud, db_models, schemas, security
from ...database import get_db
from ...dependencies import send_agent_message, get_current_active_user
from ...redis_client import get_redis
from ...core.config import settings
import redis

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    r: redis.Redis = Depends(get_redis),
):
    """
    Register a new user account.
    
    Validates input, checks for duplicates, creates user, and triggers welcome notifications.
    """
    
    # Validate email uniqueness
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password strength
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Create user
    new_user = crud.create_user(db=db, user=user)
    
    # Send user_signup event to Analytics Agent
    send_agent_message(
        recipient_id="analytics_agent",
        sender_id="mcp",
        message_content={
            "action": "record_event",
            "event_type": "user_signup",
            "user_id": str(new_user.id),
            "payload": {"email": new_user.email},
        },
        r=r,
    )
    
    # Send welcome email to Notification Agent
    send_agent_message(
        recipient_id="notification_agent",
        sender_id="mcp",
        message_content={
            "action": "process_notification_request",
            "notification_type": "welcome",
            "data": {
                "user_email": new_user.email,
                "user_name": new_user.full_name or new_user.email.split("@")[0],
            },
        },
        r=r,
    )
    
    return new_user


@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT token.
    
    Uses email as username and returns access token for subsequent API calls.
    """
    
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user(
    current_user: db_models.User = Depends(get_current_active_user),
):
    """
    Get current authenticated user's profile.
    
    Requires valid JWT token in Authorization header.
    """
    return current_user


@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(
    current_user: db_models.User = Depends(get_current_active_user),
):
    """
    Refresh JWT token for continued access.
    
    Requires valid JWT token and returns new token.
    """
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_token = security.create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": new_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(
    current_user: db_models.User = Depends(get_current_active_user),
    r: redis.Redis = Depends(get_redis),
):
    """
    Logout current user (invalidate token on client side).
    
    Note: JWT tokens don't have server-side invalidation by default.
    For true logout, client should discard the token.
    For security-critical scenarios, add token to blacklist in Redis.
    """
    
    # Optional: Add token to blacklist for extra security
    # token_blacklist_key = f"token_blacklist:{current_user.id}"
    # r.setex(token_blacklist_key, security.ACCESS_TOKEN_EXPIRE_MINUTES * 60, "true")
    
    return {"message": "Logged out successfully"}
