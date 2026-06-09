from pydantic import BaseModel


class StudentCreate(BaseModel):

    full_name: str

    parent_name: str | None = None

    parent_phone: str | None = None

    note: str | None = None

    session_fee: int

class StudentUpdate(BaseModel):

    full_name: str

    parent_name: str | None = None

    parent_phone: str | None = None

    note: str | None = None

    session_fee: int

    active: bool

class StudentResponse(BaseModel):

    id: int

    full_name: str

    parent_name: str | None

    parent_phone: str | None

    note: str | None

    session_fee: int

    active: bool

    class Config:
        from_attributes = True