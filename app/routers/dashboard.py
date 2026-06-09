from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional # Thêm import này để định nghĩa kiểu dữ liệu tùy chọn

from app.dependencies import get_db
from app.service.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("")
def dashboard(
    month: Optional[str] = None, # Tiếp nhận tham số ?month=YYYY-MM từ client
    db: Session = Depends(get_db)
):
    return DashboardService.get_dashboard(
        db=db,
        month=month # Truyền tham số xuống tầng Service
    )