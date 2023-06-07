from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from ..schemas import adminSchema
from ..database import get_db
from ..controllers import adminController, dataController, oauth2
from ..models import adminModel


router = APIRouter(
    prefix="/admin",
    tags=["Administrators"]
)

MODEL = adminModel.Admin
data_controller = dataController.DataController(model=MODEL)
controller = adminController.AdminController(data_controller=data_controller)

# get all the admins details
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[adminSchema.AdminResponse])
def get_admins(db: Session= Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = "", current_user = Depends(oauth2.get_current_user)):
    return controller.get_admins(limit=limit, skip=skip, search=search, db=db, current_user= current_user)

# create new admin
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=adminSchema.AdminResponse)
def create_admin(admin: adminSchema.AdminRequest, db: Session= Depends(get_db)):
    return controller.create_admin(admin_data=admin, db=db)
        
# get admin details by his id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=adminSchema.AdminResponse)
def get_admin(id: int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.get_admin(id=id, db=db, current_user=current_user)

# delete a admin by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(id: int, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.delete_admin(id=id, db=db, current_user=current_user)

# update the admin's details
@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= adminSchema.AdminResponse)
def update_admin(id: int, update_admin: adminSchema.AdminUpdate, db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    return controller.update_admin(id=id, updated_admin=update_admin, db=db, current_user=current_user)
    