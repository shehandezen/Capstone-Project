from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..models import courseModel
from ..controllers import dataController, oauth2, courseController
from ..schemas import courseSchema

router = APIRouter(
    prefix="/course",
    tags=['Course']
)

MODEL = courseModel.Course
data_controller = dataController.DataController(model=MODEL)
controller = courseController.CourseController(data_controller=data_controller)


# get all the course details
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[courseSchema.CourseResponse])
def get_courses(db: Session= Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    return controller.get_courses(limit=limit, skip=skip, search=search, db=db)

# create new course
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=courseSchema.CourseResponse)
def create_course(course: courseSchema.Course, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.create_course(course_data=course, db=db, current_user=current_user)

# get course details by its id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=courseSchema.CourseResponse)
def get_course(id: int, db: Session= Depends(get_db)):
    return controller.get_course(id=id, db=db)

# delete a course by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.delete_course(id=id, db=db, current_user=current_user)

# update the admin's details
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= courseSchema.CourseResponse)
def update_course(id: int, update_course: courseSchema.CourseUpdate, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.update_course(id=id, updated_course=update_course, db=db, current_user=current_user)
    