from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import schemas, models
from ..database import get_db
from .. import utils

router = APIRouter(
    prefix="/admin",
    tags=["Administrators"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.AdminResponse])
def get_admins(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    if not utils.is_query_numbers_positive(limit, skip):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Some query parameters are not valid.")
    admins = db.query(models.Admin).filter(models.Admin.name.contains(search)).limit(limit).offset(skip).all()
    return admins


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminResponse)
def create_admin(admin: schemas.AdminRequest, db: Session = Depends(get_db)):
    if utils.check_email_exist(admin.email, db, models.Admin):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"A user with email:{admin.email} already exist.")
    
    if not utils.validate_phone_number(admin.phone_number):
        raise HTTPException(status_code= status.HTTP_406_NOT_ACCEPTABLE, detail="Valid phone number required")
    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password
    new_admin = models.Admin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin
        

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.AdminResponse)
def get_admin(id: int, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A admin does not exist for id:{id}.")
    return admin

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(id: int, db:Session = Depends(get_db)):
    admin_query = db.query(models.Admin).filter(models.Admin.id == id)
    if not admin_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A admin does not exist for id:{id}.")
    admin_query.delete(synchronize_session=False)
    db.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"The admin:{id} was deleted.")

@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_admin(id: int, update_admin: schemas.AdminRequest, db: Session = Depends(get_db)):
    admin_query = db.query(models.Admin).filter(models.Admin.id == id)
    admin = admin_query.first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"A admin does not exist for id:{id}.")
    if utils.check_email_exist(update_admin.email, db, models.Admin, id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Given email is already exist.")
    admin_query.update(update_admin.dict(), synchronize_session=False)
    db.commit()
    return admin_query.first()
    