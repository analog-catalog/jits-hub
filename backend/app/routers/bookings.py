from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
router = APIRouter(tags=["Bookings"],)

@router.post("/classes/{class_id}/book", response_model=schemas.BookingResponse)
def create_bookings(class_id: int, user_id: int, db: Session = Depends(get_db)):
    user = (db.query(models.User).filter(models.User.id == user_id).first())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    class_ = (db.query(models.Class).filter(models.Class.id == class_id).first())
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    existing_booking = db.query(models.Booking).filter(models.Booking.user_id == user_id, models.Booking.class_id == class_id).first()
    if existing_booking:
        raise HTTPException(status_code=409, detail="Class already booked")

    booking_count = db.query(models.Booking).filter(models.Booking.class_id == class_id).count()

    if class_.capacity is not None and booking_count >= class_.capacity:
        raise HTTPException(status_code=409, detail="Class is full")

    booking = models.Booking(user_id=user_id, class_id=class_id)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
@router.delete("/classes/{class_id}/book")
def delete_booking(class_id: int, user_id: int, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.class_id == class_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"message" : "booking deleted"}
@router.get("/users/{user_id}/bookings", response_model=list[schemas.BookingResponse])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).filter(models.Booking.user_id == user_id).all()
    return bookings
