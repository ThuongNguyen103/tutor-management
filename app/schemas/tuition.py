from datetime import date

from pydantic import BaseModel


class TuitionCreate(BaseModel):

    student_id: int

    sessions_added: int

    amount: float

    payment_date: date

    note: str | None = None

class TuitionUpdate(BaseModel):

    sessions_added: int

    amount: float

    payment_date: date

    note: str | None = None

class TuitionResponse(BaseModel):

    id: int

    student_id: int

    sessions_added: int

    amount: float

    payment_date: date

    note: str | None

    class Config:
        from_attributes = True