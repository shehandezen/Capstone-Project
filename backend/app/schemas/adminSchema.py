from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class Admin(BaseModel):
    name: str
    dob: date
    address: str
    phone_number: str
    email: EmailStr

class AdminUpdate(Admin):
    name: Optional[str]
    dob: Optional[date]
    address: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        orm_mode = True


class AdminRequest(Admin):
    password: str

class AdminResponse(Admin):
    id: int
    created_at: datetime
    phone_number: str

    class Config:
        orm_mode = True