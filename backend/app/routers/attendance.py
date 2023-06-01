from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from ..database import get_db
from ..models import attendanceModel, classModel
from ..controllers import dataController, oauth2, attendanceController
from ..schemas import attendanceSchema

router = APIRouter(
    prefix="/attendance",
    tags=['Attendance']
)


MODEL = attendanceModel.Attendance
data_controller = dataController.DataController(model=MODEL)
controller = attendanceController.AttendanceController(data_controller=data_controller)

# get all the attendance by course
@router.get("/course/{id}", status_code=status.HTTP_200_OK, response_model=List[attendanceSchema.AttendanceResponse])
def get_attendance_by_courses(id:int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int= 20, skip:int = 0, date:date=""):
    return controller.get_attendances_by_course(model=MODEL, joined_model=classModel.Class, id_type=classModel.Class.course_id, id=id, limit=limit, skip=skip, db=db, current_user=current_user, date=date)

# get all the attendance by student
@router.get("/student/{id}", status_code=status.HTTP_200_OK, response_model=List[attendanceSchema.AttendanceResponse])
def get_attendance_by_student(id:int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int= 20, skip:int = 0):
    return controller.get_attendances_by_student(model=MODEL, joined_model=classModel.Class, id_type=classModel.Class.student_id, id=id, limit=limit, skip=skip, db=db, current_user=current_user)

# add attendance 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=attendanceSchema.AttendanceResponse)
def add_attendance(attendance_data: attendanceSchema.AttendanceRequest, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.mark_attendance(model=classModel.Class, attendance_data=attendance_data, db=db, current_user=current_user)

# update the admin's details
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= attendanceSchema.AttendanceResponse)
def update_attendance(id: int, update_attendance: attendanceSchema.AttendanceUpdate, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.update_attendance(id=id, updated_attendance=update_attendance, db=db, current_user=current_user)
    