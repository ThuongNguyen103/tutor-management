from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean
)

from app.database import Base
from sqlalchemy.orm import relationship


class Student(Base):

    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String(255),
        nullable=False
    )

    parent_name = Column(
        String(255)
    )

    parent_phone = Column(
        String(50)
    )

    note = Column(Text)

    session_fee = Column(
        Integer,
        nullable=False
    )

    active = Column(
        Boolean,
        default=True
    )

    payments = relationship(
        "TuitionPayment",
        back_populates="student"
    )