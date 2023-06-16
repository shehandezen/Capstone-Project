from pydantic import BaseModel
from datetime import date
from typing import Optional

class Attendance(BaseModel):
    student_id: int
    course_id: int
    date: date
    status: bool


class AttendanceRequest(Attendance):
    student_id: int
    course_id: int

    class Config:
        orm_mode = True

class AttendanceResponse(Attendance):
    id :int

    class Config:
        orm_mode = True

class AttendanceUpdate(BaseModel):
    date: Optional[date]
    status: Optional[bool]

    class Config:
        orm_mode = True

class AttendanceDatabase(BaseModel):
    class_id: int
    date: date
    status: bool

    class Config:
        orm_mode = True 