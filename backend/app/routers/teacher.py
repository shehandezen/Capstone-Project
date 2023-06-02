from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..models import teacherModel
from ..controllers import dataController, oauth2, teacherController
from ..schemas import teacherSchema

router = APIRouter(
    prefix="/teacher",
    tags=['Teacher']
)

MODEL = teacherModel.Teacher
data_controller = dataController.DataController(model=MODEL)
controller = teacherController.TeacherController(data_controller=data_controller)

# get all the teachers details
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[teacherSchema.TeacherResponse])
def get_teachers(db: Session= Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = "", current_user = Depends(oauth2.get_current_user)):
    return controller.get_teachers(limit=limit, skip=skip, search=search, db=db, current_user= current_user)

# create new admin
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=teacherSchema.TeacherResponse)
def create_teacher(teacher: teacherSchema.TeacherRequest, db: Session= Depends(get_db)):
    return controller.create_teacher(teacher_data=teacher, db=db)
        
# get admin details by his id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=teacherSchema.TeacherResponseAll)
def get_teacher(id: int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.get_teacher(id=id, db=db, current_user=current_user)

# delete a admin by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(id: int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.delete_teacher(id=id, db=db, current_user=current_user)

# update the admin's details
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= teacherSchema.TeacherResponse)
def update_teacher(id: int, update_teacher: teacherSchema.TeacherUpdate, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.update_teacher(id=id, updated_teacher=update_teacher, db=db, current_user=current_user)
    


