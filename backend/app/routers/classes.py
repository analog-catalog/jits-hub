from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.permissions import require_admin
from app import models, schemas

router = APIRouter(prefix="/classes", tags=["Classes"])

@router.get("/", response_model=list[schemas.ClassResponse])
def get_classes(class_type: str | None = None, db: Session = Depends(get_db)):
    classes = db.query(models.Class)
    if class_type is not None:
        classes = query.filter(models.Class.name.ilike(f"%{class_type}%"))
    return classes

@router.get("/{class_id}", response_model=schemas.ClassResponse)
def get_class(class_id: int, db: Session = Depends(get_db)):
    class_ = (db.query(models.Class).filter(models.Class.id == class_id).first())
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_

@router.post("/", response_model=schemas.ClassResponse, dependencies=[Depends(require_admin)])
def create_class(class_data: schemas.ClassCreate, user_id: int, db: Session = Depends(get_db)):
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

@router.delete("/{class_id}", dependencies=[Depends(require_admin)])
def delete_class(class_id: int, db: Session = Depends(get_db), ):
    class_ = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(class_)
    db.commit()
    return {"message" : "class deleted"}

@router.put("/{class_id}", response_model=schemas.ClassResponse)
def replace_class(class_id: int, class_data: schemas.ClassCreate, db: Session = Depends(get_db)):
    class_ = db.query(models.Class).filter(models.Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    for field, value in class_data.model_dump().items():
        setattr(class_, field, value)

    db.commit()
    db.refresh(class_)

    return class_

