from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ... import db_models, schemas
from ...database import get_db
from ...dependencies import get_current_active_user

router = APIRouter()


@router.post(
    "/admin/products",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """
    Allows a superuser to create a new product entry in the database.
    This product must correspond to a product already set up in Stripe.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can create products.",
        )

    # Check if a product with the same Stripe Price ID or Product ID already exists
    existing_product_price_id = (
        db.query(db_models.Product)
        .filter(db_models.Product.stripe_price_id == product.stripe_price_id)
        .first()
    )
    existing_product_product_id = (
        db.query(db_models.Product)
        .filter(db_models.Product.stripe_product_id == product.stripe_product_id)
        .first()
    )

    if existing_product_price_id or existing_product_product_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this Stripe Price ID or Product ID already exists.",
        )

    db_product = db_models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Log event
    # send_agent_message("analytics_agent", "admin_api", {
    #     "action": "record_event",
    #     "event_type": "product_created_by_admin",
    #     "user_id": str(current_user.id),
    #     "payload": {"product_id": str(db_product.id), "product_name": db_product.name}
    # }, get_redis())

    return db_product


@router.put("/admin/products/{product_id}", response_model=schemas.ProductResponse)
async def update_product(
    product_id: str,
    product_update: schemas.ProductCreate,  # Using ProductCreate for update for simplicity, can make a dedicated update schema
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """
    Allows a superuser to update an existing product entry.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can update products.",
        )

    db_product = (
        db.query(db_models.Product).filter(db_models.Product.id == product_id).first()
    )
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )

    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/admin/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """
    Allows a superuser to delete a product entry.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can delete products.",
        )

    db_product = (
        db.query(db_models.Product).filter(db_models.Product.id == product_id).first()
    )
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )

    db.delete(db_product)
    db.commit()
    return


@router.post("/admin/make-superuser/{user_id}", response_model=schemas.UserResponse)
async def make_user_superuser(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_active_user),
):
    """
    Allows a superuser to grant superuser privileges to another user.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can manage superuser status.",
        )

    user_to_update = (
        db.query(db_models.User).filter(db_models.User.id == user_id).first()
    )
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    user_to_update.is_superuser = True
    db.add(user_to_update)
    db.commit()
    db.refresh(user_to_update)

    print(
        f"User {user_to_update.email} granted superuser privileges by {current_user.email}."
    )
    return user_to_update
