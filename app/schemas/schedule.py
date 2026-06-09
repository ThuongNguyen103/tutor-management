from datetime import time

from pydantic import BaseModel


class ScheduleCreate(BaseModel):

    student_id: int

    day_of_week: int

    start_time: time

    end_time: time


class ScheduleUpdate(BaseModel):

    day_of_week: int

    start_time: time

    end_time: time

    active: bool


class ScheduleResponse(BaseModel):

    id: int

    student_id: int

    day_of_week: int

    start_time: time

    end_time: time

    active: bool

    class Config:
        from_attributes = True