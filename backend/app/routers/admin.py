from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db

router = APIRouter(
    prefix="/admin",
    tags=["Administrators"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminResponse)
def create_admin(admin: schemas.AdminRequest, db: Session = Depends(get_db)):
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
    admin_query.update(update_admin.dict(), synchronize_session=False)
    db.commit()
    return admin_query.first()
    