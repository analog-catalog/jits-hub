from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserResponse)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = (db.query(models.User).filter(models.User.email == user_data.email).first())
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        password_hash=user_data.password,  # TEMPORARY
        role="member",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


