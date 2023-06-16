from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class Grade(BaseModel):
    semester: str
    grade: str

class GradeRequest(Grade):
    student_id: int
    course_id: int

    class Config:
        orm_mode = True

class GradeResponse(Grade):
    id: int
    student_id: int
    course_id: int

    class Config:
        orm_mode = True

class GradeUpdate(Grade):
    semester: Optional[str]
    grade: Optional[str]

    class Config:
        orm_mode = True

class GradeDatabase(BaseModel):
    class_id: int
    semester: str
    grade: str

    class Config:
        orm_mode = True 