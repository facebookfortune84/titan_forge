from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from . import db_models, schemas
from .security import get_password_hash


def get_user(db: Session, user_id: UUID) -> Optional[db_models.User]:
    return db.query(db_models.User).filter(db_models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[db_models.User]:
    return db.query(db_models.User).filter(db_models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> db_models.User:
    hashed_password = get_password_hash(user.password)
    db_user = db_models.User(
        email=user.email, hashed_password=hashed_password, full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
