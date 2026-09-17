from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserResponse(UserBase):
    id: int
    role: str 
    model_config = {"from_attributes": True}

class ClassBase(BaseModel):
    name: str
    instructor: str
    start_time: datetime
    end_time: datetime
    capacity: int | None = None

class ClassCreate(ClassBase):
    pass

class ClassUpdate(BaseModel):
    name: str | None = None
    instructor: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    capacity: int | None = None

class ClassResponse(ClassBase):
    id: int
    model_config = {"from_attributes": True}

class BookingBase(BaseModel):
    class_id: int

class BookingResponse(BookingBase):
    id: int
    user_id: int
    booked_at: datetime

    model_config = {"from_attributes" : True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str