from pydantic import BaseModel

class Class(BaseModel):
    course_id: int
    student_id: int 

    class Config:
        orm_mode = True

class ClassResponse(Class):
    id :int

    class Config:
        orm_mode = True