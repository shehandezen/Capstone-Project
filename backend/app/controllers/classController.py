from fastapi import HTTPException, status
from .dataController import DataController
from .. import utils

class ClassController:
    def __init__(self, data_controller: DataController):
        self.data_controller = data_controller

    def add_student(self, model, class_data, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role) or utils.check_student_role(type=current_user.role):
            class_record = self.data_controller.select_two_ids(model= model, course_id=class_data.course_id, student_id=class_data.student_id, db=db)    
            if class_record:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The student with id:{class_data.student_id} is already following course id:{class_data.course_id}")
            if utils.check_student_role(type=current_user.role):
                if not class_data.student_id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")
            return self.data_controller.insert_data(class_data, db=db)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")


    def remove_student(self, model, course_id, student_id, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role) or utils.check_student_role(type=current_user.role):
            class_record = self.data_controller.select_two_ids(model= model, course_id=course_id, student_id=student_id, db=db)    
            if not class_record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The student with id:{student_id} is not following course id:{course_id}")
            if utils.check_student_role(type=current_user.role):
                if not student_id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            if self.data_controller.delete_record(id=class_record.id, db=db):
                return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The student:{student_id} was unenrolled from course id:{course_id}.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")
