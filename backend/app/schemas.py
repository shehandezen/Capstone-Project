from pydantic import BaseModel, EmailStr
from datetime import date, datetime

class Admin(BaseModel):
    name: str
    dob: date
    address: str
    phone_number: str
    manager: int
    email: EmailStr

class AdminRequest(Admin):
    password: str

class AdminResponse(Admin):
    id: int
    created_at: datetime
    phone_number: int

    class Config:
        orm_mode = True

