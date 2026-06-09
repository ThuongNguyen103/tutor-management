from sqlalchemy import (
    Column,
    Integer,
    Date,
    Numeric,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship

from app.database import Base


class TuitionPayment(Base):

    __tablename__ = "tuitions"

    id = Column(
        Integer,
        primary_key=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    sessions_added = Column(
        Integer,
        nullable=False
    )

    amount = Column(
        Numeric(12, 0),
        nullable=False
    )

    payment_date = Column(
        Date,
        nullable=False
    )

    note = Column(Text)

    student = relationship(
        "Student",
        back_populates="payments"
    )