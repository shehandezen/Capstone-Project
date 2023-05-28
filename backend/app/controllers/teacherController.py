from fastapi import HTTPException, status
from .dataController import DataController
from .. import utils
from ..schemas import teacherSchema

class TeacherController:
    def __init__(self, data_controller: DataController):
        self.data_controller = data_controller

    def get_teachers(self, limit, skip, search, db, current_user):
        if utils.check_admin_role(type=current_user.role):
            if not utils.is_query_numbers_positive(limit, skip):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail="Some query parameters are not valid.")
            return self.data_controller.get_all_data_with_query(search=search, skip=skip, limit=limit, db=db)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def get_teacher(self, id, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            if utils.check_teacher_role(type=current_user.role):
                if not id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            teacher = self.data_controller.get_data(id=id, db=db)
            if not teacher:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A teacher does not exist for id:{id}.")
            return teacher
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def create_teacher(self, teacher_data, db):
        if self.data_controller.check_email_exist(teacher_data.email, db=db):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"A user with email:{teacher_data.email} already exist.")
        
        if not utils.validate_phone_number(teacher_data.phone_number):
            raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE, detail="Valid phone number required")
        hashed_password = utils.hash(teacher_data.password)
        teacher_data.password = hashed_password
        return self.data_controller.insert_data(teacher_data, db=db)

    def delete_teacher(self, id, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            if utils.check_teacher_role(type=current_user.role):
                if not id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            if not self.data_controller.get_data(id=id, db=db):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A teacher does not exist for id:{id}.")
            if self.data_controller.delete_record(id=id, db=db):
                return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The teacher:{id} was deleted.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def update_teacher(self, id, updated_teacher, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            if utils.check_teacher_role(type=current_user.role):
                if not id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            teacher = self.data_controller.get_data(id=id, db=db)
            if not teacher:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A teacher does not exist for id:{id}.")
            if self.data_controller.check_email_exist(email=updated_teacher.email, id=id, db=db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Given email is already exist.")
            updated_teacher = utils.update_dict(teacher, updated_teacher.dict(), update_schema=teacherSchema.TeacherUpdate)
            return self.data_controller.update_data(id=id, updated_data=updated_teacher, db=db)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")
    