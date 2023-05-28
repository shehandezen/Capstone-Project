from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class Student(BaseModel):
    name: str
    dob: date
    address: str
    parent_name: str
    parent_phone_number: str
    email: EmailStr

class StudentUpdate(Student):
    name: Optional[str]
    dob: Optional[date]
    address: Optional[str]
    parent_name: Optional[str]
    parent_phone_number: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        orm_mode = True


class StudentRequest(Student):
    password: str

class StudentResponse(Student):
    id: int
    parent_phone_number: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True