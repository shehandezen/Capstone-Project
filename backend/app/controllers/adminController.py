from fastapi import HTTPException, status
from ..models import adminModel
from .. import utils



def get_admins(db, limit, skip, search):
    if not utils.is_query_numbers_positive(limit, skip):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Some query parameters are not valid.")
    admins = db.query(adminModel.Admin).filter(
        adminModel.Admin.name.contains(search)).limit(limit).offset(skip).all()
    return admins

def create_admin(admin, db):
    if utils.check_email_exist(admin.email, db, adminModel.Admin):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"A user with email:{admin.email} already exist.")
    
    if not utils.validate_phone_number(admin.phone_number):
        raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE, detail="Valid phone number required")
    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password
    new_admin = adminModel.Admin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def get_admin(id, db):
    admin = db.query(adminModel.Admin).filter(adminModel.Admin.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A admin does not exist for id:{id}.")
    return admin

def delete_admin(id, db):
    admin_query = db.query(adminModel.Admin).filter(adminModel.Admin.id == id)
    if not admin_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A admin does not exist for id:{id}.")
    admin_query.delete(synchronize_session=False)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The admin:{id} was deleted.")

def update_admin(id, update_admin, db):
    admin_query = db.query(adminModel.Admin).filter(adminModel.Admin.id == id)
    admin = admin_query.first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A admin does not exist for id:{id}.")
    if utils.check_email_exist(update_admin.email, db, adminModel.Admin, id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Given email is already exist.")
    updated_admin = utils.update_dict(admin, update_admin.dict())
    admin_query.update(updated_admin, synchronize_session=False)
    db.commit()
    return admin_query.first()