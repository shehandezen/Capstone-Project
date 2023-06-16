from ..database import Base
from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

class Attendance(Base):
    __tablename__ = "attendance"
    id =  Column(Integer, primary_key=True, nullable=False)
    class_id = Column(Integer, ForeignKey("class.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Boolean, nullable=False)
    classroom = relationship("Class")