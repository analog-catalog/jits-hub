from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/classes", tags=["Classes"])

@router.get("/", response_model=list[schemas.ClassResponse])
def get_classes(db: Session = Depends(get_db)):
    return db.query(models.Class).all()

@router.post("/", response_model=schemas.ClassResponse)
def create_class(class_data: schemas.ClassCreate, db: Session = Depends(get_db)):
    new_class = models.Class(**class_data.model_dump())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

@router.patch("/{class_id}")
def update_class():
    ...

@router.delete("/{class_id}")
def delete_class():
    ...