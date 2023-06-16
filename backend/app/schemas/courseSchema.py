from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Course(BaseModel):
    name: str
    description: str
    teacher_id: Optional[int]

class CourseUpdate(Course):
    name: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True

class CourseResponse(Course):
    id: int
    teacher_id: int
    created_at: datetime
 

    class Config:
        orm_mode = True