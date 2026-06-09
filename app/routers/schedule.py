from fastapi import APIRouter, Depends, HTTPException
from datetime import date, time
from requests import Session

from app.dependencies import get_db
from app.service.schedule_service import ScheduleService
from app.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleUpdate

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"]
)

@router.get(
    "/today"
)
def get_today_schedules(
    db: Session = Depends(get_db)
):

    return ScheduleService.get_today(db)

@router.get("/by-date")
def get_schedules_by_date(
    schedule_date: date,
    db: Session = Depends(get_db)
):

    return ScheduleService.get_by_date(
        db,
        schedule_date
    )

@router.get(
    "/week"
)
def get_week_schedule(
    db: Session = Depends(get_db)
):

    return ScheduleService.get_week_schedule(db)

@router.get(
    "",
    response_model=list[ScheduleResponse]
)
def get_schedules(
    db: Session = Depends(get_db)
):
    return ScheduleService.get_all(db)

@router.get(
    "/{schedule_id}",
    response_model=ScheduleResponse
)
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):

    schedule = ScheduleService.get_by_id(
        db,
        schedule_id
    )

    if not schedule:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found"
        )

    return schedule

@router.post(
    "",
    response_model=ScheduleResponse
)
def create_schedule(
    payload: ScheduleCreate,
    db: Session = Depends(get_db)
):

    if ScheduleService.check_conflict(
        db,
        payload
    ):
        raise HTTPException(
            status_code=400,
            detail="Schedule conflict"
        )

    return ScheduleService.create(
        db,
        payload
    )

@router.put(
    "/{schedule_id}",
    response_model=ScheduleResponse
)
def update_schedule(
    schedule_id: int,
    payload: ScheduleUpdate,
    db: Session = Depends(get_db)
):

    schedule = ScheduleService.get_by_id(
        db,
        schedule_id
    )

    if not schedule:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found"
        )

    return ScheduleService.update(
        db,
        schedule,
        payload
    )

@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):

    schedule = ScheduleService.get_by_id(
        db,
        schedule_id
    )

    if not schedule:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found"
        )

    ScheduleService.delete(
        db,
        schedule
    )

    return {
        "message": "Deleted"
    }

@router.get(
    "/dashboard/today"
)
def dashboard_today(
    db: Session = Depends(get_db)
):

    return ScheduleService.today_summary(
        db
    )