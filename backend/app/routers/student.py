from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..controllers import dataController, studentController, oauth2
from ..models import studentModel, courseModel
from ..schemas import studentSchema


router = APIRouter(
    prefix='/student',
    tags=['Student']
)

MODEL = studentModel.Student
data_controller = dataController.DataController(model=MODEL)
controller = studentController.StudentController(data_controller=data_controller)

# get all the students details
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[studentSchema.StudentResponse])
def get_students(db: Session= Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = "", current_user = Depends(oauth2.get_current_user)):
    return controller.get_students(limit=limit, skip=skip, search=search, db=db, current_user= current_user)

# create new student
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=studentSchema.StudentResponse)
def create_student(student: studentSchema.StudentRequest, db: Session= Depends(get_db)):
    return controller.create_student(student_data=student, db=db)
        

# get student details by his id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=studentSchema.StudentResponseAll)
def get_student(id: int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.get_student(model=courseModel.Course ,id=id, db=db, current_user=current_user)

# delete a student by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(id: int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.delete_student(id=id, db=db, current_user=current_user)

# update the admin's details
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= studentSchema.StudentResponse)
def update_student(id: int, update_student: studentSchema.StudentUpdate, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.update_student(id=id, updated_student=update_student, db=db, current_user=current_user)
    
