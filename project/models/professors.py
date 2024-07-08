from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from .middle_tables import professor_lesson_association, student_professor_association


class Professor(Base):
    __tablename__ = "professors"
    LID = Column(Integer, unique=True, primary_key=True)
    Fname = Column(String)
    Lname = Column(String)
    ID = Column(String, unique=True)
    Department = Column(String)
    Major = Column(String)
    Birth = Column(String)
    BornCity = Column(String)
    Address = Column(String)
    PostalCode = Column(String)
    CPhone = Column(String)
    HPhone = Column(String)
    Lesson_ids = Column(String)

    LCourseIDs = relationship(
        "Lesson", secondary=professor_lesson_association, back_populates="professor"
    )
    student = relationship(
        "Student", secondary=student_professor_association, back_populates="LIDs"
    )

    def get_fullname(self):
        return f"{self.Fname} {self.Lname}"
