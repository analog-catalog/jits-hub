from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/classes", tags=["Classes"])

@router.get("/", response_model=list[schemas.ClassResponse])
def get_classes(db: Session = Depends(get_db)):
    return db.query(models.Class).all()

@router.get("/{class_id}", response_model=schemas.ClassResponse)
def get_class(class_id: int, db: Session = Depends(get_db)):
    class_ = (db.query(models.Class).filter(models.Class.id == class_id).first())
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_

@router.post("/", response_model=schemas.ClassResponse)
def create_class(class_data: schemas.ClassCreate, db: Session = Depends(get_db)):
    new_class = models.Class(**class_data.model_dump())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

@router.patch("/{class_id}")
def update_class(class_id: int, class_data: schemas.ClassUpdate, db: Session = Depends(get_db)):
    class_ = (db.query(models.Class).filter(models.Class.id == class_id).first())
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    updates = class_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(class_, field, value)
    db.commit()
    db.refresh(class_)
    return class_

@router.delete("/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    class_ = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(class_)
    db.commit()
    return {"message" : "class deleted"}

