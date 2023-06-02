from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..database import get_db
from ..models import gradeModel, classModel
from ..controllers import dataController, oauth2, gradeController
from ..schemas import gradeSchema

router = APIRouter(
    prefix="/grade",
    tags=['Grade']
)

MODEL = gradeModel.Grade
data_controller = dataController.DataController(model=MODEL)
controller = gradeController.GradeController(data_controller=data_controller)

# get all the grade by course
@router.get("/course/{id}", status_code=status.HTTP_200_OK, response_model=List[gradeSchema.GradeResponse])
def get_grade_by_course(id:int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int= 20, skip:int = 0):
    return controller.get_grades(model=MODEL, joined_model=classModel.Class, id_type=classModel.Class.course_id, id=id, limit=limit, skip=skip, db=db, current_user=current_user)

# get all the grade by student
@router.get("/student/{id}", status_code=status.HTTP_200_OK, response_model=List[gradeSchema.GradeResponse])
def get_grade_by_student(id:int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int= 20, skip:int = 0):
    return controller.get_grades(model=MODEL, joined_model=classModel.Class, id_type=classModel.Class.student_id, id=id, limit=limit, skip=skip, db=db, current_user=current_user)

# add attendance 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=gradeSchema.GradeResponse)
def add_attendance(grade_data: gradeSchema.GradeRequest, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.add_grade(model=classModel.Class, grade_data=grade_data, db=db, current_user=current_user)


# update the grade details
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= gradeSchema.GradeResponse)
def update_grade(id: int, update_grade: gradeSchema.GradeUpdate, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.update_grade(id=id, updated_grade=update_grade, db=db, current_user=current_user)
    