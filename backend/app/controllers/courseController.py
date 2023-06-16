from fastapi import HTTPException, status
from .dataController import DataController
from .. import utils
from ..schemas import courseSchema

class CourseController:
    def __init__(self, data_controller: DataController):
        self.data_controller = data_controller

    def get_courses(self, limit, skip, search, db):
        if not utils.is_query_numbers_positive(limit, skip):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail="Some query parameters are not valid.")
        return self.data_controller.get_all_data_with_query(search=search, skip=skip, limit=limit, db=db)
        
    def create_course(self, course_data, db, current_user):
        if utils.check_admin_role(type=current_user.role):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="administrators can not create courses.")
        if utils.check_teacher_role(type=current_user.role):
            course_data.teacher_id = current_user.id
            return self.data_controller.insert_data(course_data, db=db)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def get_course(self, id, db):
        course = self.data_controller.get_data(id=id, db=db)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A course does not exist for id:{id}.")
        return course
        
    def delete_course(self, id, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            course = self.data_controller.get_data(id=id, db=db)
            if not course:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A course does not exist for id:{id}.")
            if utils.check_teacher_role(type=current_user.role):
                if not course.teacher_id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            if self.data_controller.delete_record(id=id, db=db):
                return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The course:{id} was deleted.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def update_course(self, id, updated_course, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            course = self.data_controller.get_data(id=id, db=db)
            if not course:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A course does not exist for id:{id}.")
            if utils.check_teacher_role(type=current_user.role):
                if not course.teacher_id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            updated_course = utils.update_dict(course, updated_course.dict(), update_schema=courseSchema.CourseUpdate)
            return self.data_controller.update_data(id=id, updated_data=updated_course, db=db)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")
            