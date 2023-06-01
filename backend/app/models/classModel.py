from ..database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Class(Base):
    __tablename__ = "class"
    id =  Column(Integer, primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE"), nullable=False)
    course = relationship("Course")
    student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"), nullable=False)
    student = relationship("Student")