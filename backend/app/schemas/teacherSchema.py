from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class Teacher(BaseModel):
    name: str
    dob: date
    address: str
    phone_number: str
    email: EmailStr

class TeacherUpdate(Teacher):
    name: Optional[str]
    dob: Optional[date]
    address: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        orm_mode = True


class TeacherRequest(Teacher):
    password: str

class TeacherResponse(Teacher):
    id: int
    created_at: datetime
    phone_number: str

    class Config:
        orm_mode = True