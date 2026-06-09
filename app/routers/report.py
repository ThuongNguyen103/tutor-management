from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.service.report_service import (
    ReportService
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get(
    "/monthly-revenue"
)
def monthly_revenue(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):

    return (
        ReportService
        .monthly_revenue(
            db,
            year,
            month
        )
    )

@router.get(
    "/monthly-lessons"
)
def monthly_lessons(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):

    return (
        ReportService
        .monthly_lessons(
            db,
            year,
            month
        )
    )