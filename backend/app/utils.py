import phonenumbers as phone
from passlib.context import CryptContext


def validate_phone_number(number: str):
    try:
        phone_number = phone.parse(number=number)
        return phone.is_valid_number(phone_number)
    except:
        return False

def check_email_exist(email, db, entity, id = 0):
      return db.query(entity).filter(entity.email == email, entity.id != id).first()
    
def is_query_numbers_positive(*params):
    for param in params:
        if not type(param) == int:
            return False
        if param < 0:
            return False
    return True

passwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated= "auto"
)

def hash(password:str):
    return passwd_context.hash(password)

def verify(plain_password, hashed_password):
    return passwd_context.verify(plain_password, hashed_password)