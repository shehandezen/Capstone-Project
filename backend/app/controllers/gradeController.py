from fastapi import HTTPException, status
from .dataController import DataController
from .. import utils
from ..schemas import gradeSchema
from ..models import studentModel, courseModel, classModel


class GradeController:
    def __init__(self, data_controller: DataController):
        self.data_controller = data_controller

    def get_grades(self, model, joined_model, id_type, id, limit, skip, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role) or utils.check_student_role(type=current_user.role):
            if not utils.is_query_numbers_positive(limit):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                        detail="Some query parameters are not valid.")
            if utils.check_student_role(type=current_user.role):
                if not self.data_controller.get_data(id=id, db=db, model=studentModel.Student):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The student with id:{id} does not exist.")
                if not current_user.id == int(id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")
            if id_type == classModel.Class.course_id:
                if not self.data_controller.get_data(id=id, db=db, model=courseModel.Course):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The course with id:{id} does not exist.")
            else:
                if not self.data_controller.get_data(id=id, db=db, model=studentModel.Student):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The student with id:{id} does not exist.")
            return self.data_controller.get_multiple_grade_records_by_join(model_id=model.class_id, joined_model=joined_model, id_type=id_type, id=id, limit=limit, skip=skip, db=db, other_condition=True)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")   

    def add_grade(self, model, grade_data, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            if utils.check_teacher_role(type=current_user.role):
                course = self.data_controller.get_data(id=grade_data.course_id, db=db, model=courseModel)
                if not course.teacher_id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            class_record = self.data_controller.select_two_ids(model= model, course_id=grade_data.course_id, student_id=grade_data.student_id, db=db)    
            if not class_record:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The student with id:{grade_data.student_id} is not following course id:{grade_data.course_id}")
            class_id = class_record.id
            if self.data_controller.check_semester_column_exist(id=class_id, semester=grade_data.semester, db=db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="That grade record already exist.")
            grade = gradeSchema.GradeDatabase(class_id=class_id, semester=grade_data.semester, grade=grade_data.grade)
            response_data = self.data_controller.insert_data(grade, db=db)
            return gradeSchema.GradeResponse(semester=response_data.semester, grade=response_data.grade, id=response_data.id, student_id=grade_data.student_id, course_id=grade_data.course_id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def update_grade(self, id, updated_grade, db, current_user):
        if utils.check_admin_role(type=current_user.role) or utils.check_teacher_role(type=current_user.role):
            grade = self.data_controller.get_data(id=id, db=db)
            if not grade:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A grade record does not exist for id:{id}.")
            if utils.check_teacher_role(type=current_user.role):
                course = self.data_controller.get_data(id=updated_grade.course_id, db=db, model=courseModel)
                if not course.teacher_id == int(current_user.id):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            updated_grade = utils.update_dict(grade, updated_grade.dict(), update_schema=gradeSchema.GradeUpdate)
            response = self.data_controller.update_data(id=id, updated_data=updated_grade, db=db)
            get_class_data = self.data_controller.get_data(response.class_id, db, classModel.Class)
            return gradeSchema.GradeResponse(student_id=get_class_data.student_id, course_id=get_class_data.course_id, semester=response.semester, grade=response.grade, id=response.id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")
            