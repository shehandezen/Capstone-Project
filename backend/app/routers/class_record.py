from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import classModel
from ..controllers import dataController, oauth2, classController
from ..schemas import classSchema

router = APIRouter(
    prefix="/class",
    tags=['Class']
)

MODEL = classModel.Class
data_controller = dataController.DataController(model=MODEL)
controller = classController.ClassController(data_controller=data_controller)

# add student to class
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=classSchema.ClassResponse)
def add_student(class_data: classSchema.Class, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.add_student(model=MODEL, class_data=class_data, db=db, current_user=current_user)

# remove student from class
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def remove_student(course_id:int, student_id:int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.remove_student(model=MODEL, course_id=course_id, student_id=student_id, db=db, current_user=current_user)


