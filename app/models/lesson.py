from sqlalchemy import (
    Column,
    Integer,
    Date,
    Text,
    Boolean,
    ForeignKey
)

from app.database import Base


class Lesson(Base):

    __tablename__ = "lessons"

    id = Column(
        Integer,
        primary_key=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    lesson_date = Column(
        Date,
        nullable=False
    )

    content = Column(
        Text
    )

    completed = Column(
        Boolean,
        default=True
    )