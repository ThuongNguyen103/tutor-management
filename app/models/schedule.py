from sqlalchemy import (
    Column,
    Integer,
    Time,
    ForeignKey,
    Boolean
)

from app.database import Base


class Schedule(Base):

    __tablename__ = "schedules"

    id = Column(
        Integer,
        primary_key=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    day_of_week = Column(
        Integer,
        nullable=False
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
        nullable=False
    )

    active = Column(
        Boolean,
        default=True
    )