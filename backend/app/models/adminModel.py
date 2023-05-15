from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Admin(Base):
    __tablename__ = "administrator"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    manager = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )

