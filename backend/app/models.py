from sqlalchemy import Column, Integer, String, Boolean, Date
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    instructor = Column(String(100), nullable=False)
    start_time = Column(Date)
    end_time = Column(Date)
    capacity = Column(Integer)

class Booking(Base):
    __tablename__ = "bookings"
    user_id = Column(Integer, primary_key=True)
    class_id = Column(Integer, primary_key=True)

