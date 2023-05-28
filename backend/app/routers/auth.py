from fastapi import Depends, APIRouter, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import adminModel
from ..controllers import authController

router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

class ExtendedOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
        type: str

# user login endpoint
@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def login( type:str, user_credentials: ExtendedOAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   return authController.login_user(user_credentials, db, type)