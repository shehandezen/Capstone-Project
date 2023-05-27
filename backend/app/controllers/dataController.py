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
    def get_data(self, id, db):
       return db.query(self.model).filter(self.model.id == id).first()

    # select all data according to query parameters
    def get_all_data_with_query(self, search, limit, skip, db):
       return db.query(self.model).filter(self.model.name.contains(search)).limit(limit).offset(skip).all()

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
