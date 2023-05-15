from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from ..schemas import adminSchema
from ..database import get_db
from ..controllers import adminController
from ..controllers import oauth2
from ..models import adminModel

router = APIRouter(
    prefix="/admin",
    tags=["Administrators"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[adminSchema.AdminResponse])
def get_admins(db: Session = Depends(get_db), current_user:str = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    return adminController.get_admins(db, limit, skip, search)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=adminSchema.AdminResponse)
def create_admin(admin: adminSchema.AdminRequest, db: Session = Depends(get_db)):
    return adminController.create_admin(admin, db)
        

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=adminSchema.AdminResponse)
def get_admin(id: int, db: Session = Depends(get_db)):
    return adminController.get_admin(id, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(id: int, db:Session = Depends(get_db)):
    return adminController.delete_admin(id, db)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= adminSchema.AdminResponse)
def update_admin(id: int, update_admin: adminSchema.AdminUpdate, db: Session = Depends(get_db)):
    return adminController.update_admin(id, update_admin, db)
    