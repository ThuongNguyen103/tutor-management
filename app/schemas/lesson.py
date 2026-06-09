from datetime import date

from pydantic import BaseModel


class LessonCreate(BaseModel):

    student_id: int

    lesson_date: date

    content: str

    completed: bool = True

class LessonUpdate(BaseModel):

    lesson_date: date

    content: str

    completed: bool

class LessonResponse(BaseModel):

    id: int

    student_id: int

    lesson_date: date

    content: str

    completed: bool

    class Config:
        from_attributes = True