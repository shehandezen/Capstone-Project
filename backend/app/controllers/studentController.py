from fastapi import HTTPException, status
from .dataController import DataController
from .. import utils
from ..schemas import studentSchema

class StudentController:
    def __init__(self, data_controller: DataController):
        self.data_controller = data_controller

    def get_students(self, limit, skip, search, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            if not utils.is_query_numbers_positive(limit, skip):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail="Some query parameters are not valid.")
            return self.data_controller.get_all_data_with_query(search=search, skip=skip, limit=limit, db=db)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    
    def get_student(self, id, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role) or utils.check_student_role(type=current_user.role):
            if utils.check_student_role(type=current_user.role):
                if not id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            student = self.data_controller.get_data(id=id, db=db)
            if not student:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A student does not exist for id:{id}.")
            return student
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def create_student(self, student_data, db):
        if self.data_controller.check_email_exist(student_data.email, db=db):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"A user with email:{student_data.email} already exist.")
        
        if not utils.validate_phone_number(student_data.parent_phone_number):
            raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE, detail="Valid phone number required")
        hashed_password = utils.hash(student_data.password)
        student_data.password = hashed_password
        return self.data_controller.insert_data(student_data, db=db)

    def delete_student(self, id, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            if not self.data_controller.get_data(id=id, db=db):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A stduent does not exist for id:{id}.")
            if self.data_controller.delete_record(id=id, db=db):
                return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The student:{id} was deleted.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    
    def update_student(self, id, updated_student, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role) or utils.check_student_role(type=current_user.role):
            if utils.check_student_role(type=current_user.role):
                if not id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            student = self.data_controller.get_data(id=id, db=db)
            if not student:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A student does not exist for id:{id}.")
            if self.data_controller.check_email_exist(email=updated_student.email, id=id, db=db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Given email is already exist.")
            updated_student = utils.update_dict(student, updated_student.dict(), update_schema=studentSchema.StudentUpdate)
            return self.data_controller.update_data(id=id, updated_data=updated_student, db=db)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")