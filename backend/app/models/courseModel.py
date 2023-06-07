from ..database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Course(Base):
    __tablename__ = "course"
    id =  Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()') )
    teacher_id = Column(Integer, ForeignKey("teacher.id", ondelete="CASCADE"), nullable=False)
    teacher = relationship("Teacher")
