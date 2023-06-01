from fastapi import HTTPException, status
from .dataController import DataController
from ..models import studentModel, courseModel, classModel
from .. import utils
from ..schemas import attendanceSchema

class AttendanceController:
    def __init__(self, data_controller: DataController):
        self.data_controller = data_controller
        

    def get_attendances_by_course(self, model, joined_model, id_type, id, limit, skip, db, current_user, date=""):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            if not utils.is_query_numbers_positive(limit):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                        detail="Some query parameters are not valid.")
    
            if date == "":
                condition = True
            else:
                condition = (model.date == date)
            return self.data_controller.get_multiple_records_by_join(model_id=model.class_id, joined_model=joined_model, id_type=id_type, id=id, limit=limit, skip=skip, db=db, other_condition=condition)
            
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def get_attendances_by_student(self, model, joined_model, id_type, id, limit, skip, db, current_user, date=""):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            if not utils.is_query_numbers_positive(limit):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                        detail="Some query parameters are not valid.")
            if not self.data_controller.get_data(id=id, db=db, model=studentModel.Student):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The student with id:{id} does not exist.")
            if date == "":
                condition = True
            else:
                condition = (model.date == date)
            return self.data_controller.get_multiple_records_by_join(model_id=model.class_id, joined_model=joined_model, id_type=id_type, id=id, limit=limit, skip=skip, db=db, other_condition=condition)
            
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")
  

    def mark_attendance(self, model, attendance_data, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            if utils.check_teacher_role(type=current_user.role):
                course = self.data_controller.get_data(id=attendance_data.course_id, db=db, model=courseModel)
                if not course.teacher_id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            class_record = self.data_controller.select_two_ids(model= model, course_id=attendance_data.course_id, student_id=attendance_data.student_id, db=db)    
            if not class_record:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The student with id:{attendance_data.student_id} is not following course id:{attendance_data.course_id}")
            class_id = class_record.id
            if self.data_controller.check_record_exist(id=class_id, date=attendance_data.date, db=db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="That attendance record already exist.")
            attendance = attendanceSchema.AttendanceDatabase(class_id=class_id, date=attendance_data.date, status=attendance_data.status)
            response_data = self.data_controller.insert_data(attendance, db=db)
            return attendanceSchema.AttendanceResponse(student_id=attendance_data.student_id, course_id=attendance_data.course_id, date=response_data.date, status=response_data.status, id=response_data.id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def update_attendance(self, id, updated_attendance, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            attendance = self.data_controller.get_data(id=id, db=db)
            if not attendance:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A attendance record does not exist for id:{id}.")
            if utils.check_teacher_role(type=current_user.role):
                course = self.data_controller.get_data(id=updated_attendance.course_id, db=db, model=courseModel)
                if not course.teacher_id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            updated_attendance = utils.update_dict(attendance, updated_attendance.dict(), update_schema=attendanceSchema.AttendanceUpdate)
            response = self.data_controller.update_data(id=id, updated_data=updated_attendance, db=db)
            get_class_data = self.data_controller.get_data(response.class_id, db, classModel.Class)
            return attendanceSchema.AttendanceResponse(student_id=get_class_data.student_id, course_id=get_class_data.course_id, date=response.date, status=response.status, id=response.id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")
            