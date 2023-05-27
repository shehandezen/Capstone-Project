import phonenumbers as phone
from passlib.context import CryptContext
from .schemas import adminSchema
from fastapi import HTTPException, status


# validate the phone number
def validate_phone_number(number: str):
    try:
        phone_number = phone.parse(number=number)
        return phone.is_valid_number(phone_number)
    except:
        return False

# check if the user enters negative values for the query parameters   
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

# plain password text covert to the hashed password
def hash(password:str):
    return passwd_context.hash(password)

# verify the user entered password
def verify(plain_password, hashed_password):
    return passwd_context.verify(plain_password, hashed_password)

# update the dictionary by updated data dictionary
def update_dict(object, data):
    object_py = adminSchema.AdminUpdate.from_orm(object)
    object_dict = object_py.dict()
    for i in data:
        for j in object_dict:
            if i == j:
                if not data[i] == None:
                    if i == "password":
                        object_dict[j] = hash(data[i])
                        continue
                    object_dict[j] = data[i]
    return object_dict

def check_admin_role(type):
    if type == 'admin':
        return True
    return False
    