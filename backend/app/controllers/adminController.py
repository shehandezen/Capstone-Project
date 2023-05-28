from fastapi import HTTPException, status
from .. import utils
from .dataController import DataController
from ..schemas import adminSchema


class AdminController:
    def __init__(self, data_controller: DataController):
        self.data_controller = data_controller

    def get_admins(self, limit, skip, search, db, current_user):
        if utils.check_admin_role(type=current_user.role):
            if not utils.is_query_numbers_positive(limit, skip):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail="Some query parameters are not valid.")
            return self.data_controller.get_all_data_with_query(search=search, skip=skip, limit=limit, db=db)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")
        

    def create_admin(self, admin_data, db):
        if self.data_controller.check_email_exist(admin_data.email, db=db):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"A user with email:{admin_data.email} already exist.")
        
        if not utils.validate_phone_number(admin_data.phone_number):
            raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE, detail="Valid phone number required")
        hashed_password = utils.hash(admin_data.password)
        admin_data.password = hashed_password
        return self.data_controller.insert_data(admin_data, db=db)

    def get_admin(self, id, db, current_user):
        if utils.check_admin_role(type=current_user.role):
            admin = self.data_controller.get_data(id=id, db=db)
            if not admin:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A admin does not exist for id:{id}.")
            return admin
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def delete_admin(self, id, db, current_user):
        if utils.check_admin_role(type=current_user.role):
            if not id == int(current_user.id):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            if not self.data_controller.get_data(id=id, db=db):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A admin does not exist for id:{id}.")
            if self.data_controller.delete_record(id=id, db=db):
                return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The admin:{id} was deleted.")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")

    def update_admin(self, id, updated_admin, db, current_user):
        if utils.check_admin_role(type=current_user.role):
            if not id == int(current_user.id):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action.")
            admin = self.data_controller.get_data(id=id, db=db)
            if not admin:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A admin does not exist for id:{id}.")
            if self.data_controller.check_email_exist(email=updated_admin.email, id=id, db=db):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Given email is already exist.")
            updated_admin = utils.update_dict(admin, updated_admin.dict(), update_schema=adminSchema.AdminUpdate)
            return self.data_controller.update_data(id=id, updated_data=updated_admin, db=db)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested task.")
            