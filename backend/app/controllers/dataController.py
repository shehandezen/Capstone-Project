class DataController:
    def __init__(self, model):
        self.model = model


    # data insert to the databse
    def insert_data(self, data, db):
        created_record = self.model(**data.dict())
        db.add(created_record)
        db.commit()
        db.refresh(created_record) ##
        return created_record

    # select data using given id
    def get_data(self, id, db, model=None):
        if model is None:
            model = self.model
        return db.query(model).filter(model.id == id).first()

    # select all data according to query parameters
    def get_all_data_with_query(self, limit, db, search="", skip=0):
       return db.query(self.model).filter(self.model.name.contains(search)).limit(limit).offset(skip).all()


# select class.course_id, class.student_id, attendance.date, attendance.status from attendance left join class on attendance.class_id = class.id where class.course_id = {id}
#  db.query(self.model, joined_model).join(joined_model, joined_model.id == self.model.class_id, isouter=True).filter(joined_model.course_id == id).limit(limit).offset(skip).all()
    def get_multiple_records_by_join(self, model_id, joined_model, id_type, id, limit, skip, db, other_condition):
        
        return db.query(self.model.id, self.model.date, self.model.status, joined_model.course_id,joined_model.student_id).join(joined_model, joined_model.id == model_id , isouter=True).filter(other_condition, id_type == id ).limit(limit).offset(skip).all()

    # update a database record using given id
    def update_data(self, id, updated_data, db):
        db.query(self.model).filter(self.model.id == id).update(updated_data, synchronize_session=False)
        db.commit()
        return self.get_data(id=id, db=db)

    # delete a record by id
    def delete_record(self, id, db):
        delete_record = db.query(self.model).filter(self.model.id == id).delete(synchronize_session=False)
        db.commit()
        return True

    # check the given email address is already exist in the database
    def check_email_exist(self, email, db, id=0):
        return db.query(self.model).filter(self.model.email == email, self.model.id != id).first()

    def select_two_ids(self, model, course_id, student_id, db):
        return db.query(model).filter(model.course_id == course_id, model.student_id == student_id).first()

    def check_record_exist(self, id, date, db):
        return db.query(self.model).filter(self.model.class_id == id , self.model.date ==date).first()
