from datetime import date, datetime
from typing import Optional # Thêm import này nếu chưa có

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.lesson import Lesson
from app.models.schedule import Schedule
from app.service.student_service import StudentService

class DashboardService:

    @staticmethod
    def get_dashboard(
        db: Session,
        month: Optional[str] = None  # Nhận tham số month từ router
    ):

        total_students = (
            db.query(Student)
            .filter(Student.active == True)
            .count()
        )

        today_weekday = datetime.now().isoweekday()

        today_classes = (
            db.query(Schedule)
            .filter(
                Schedule.day_of_week == today_weekday,
                Schedule.active == True
            )
            .count()
        )

        today = date.today()
        
        # Mặc định mục tiêu thống kê là năm và tháng hiện tại
        target_year = today.year
        target_month = today.month

        # Nếu có tháng được truyền lên từ frontend (Định dạng: "YYYY-MM")
        if month:
            try:
                parsed_date = datetime.strptime(month, "%Y-%m")
                target_year = parsed_date.year
                target_month = parsed_date.month
            except ValueError:
                # Nếu chuỗi truyền lên lỗi định dạng, giữ nguyên tháng hiện tại
                pass

        today_revenue = (
            db.query(
                func.coalesce(
                    func.sum(Student.session_fee),
                    0
                )
            )
            .join(
                Lesson,
                Lesson.student_id == Student.id
            )
            .filter(
                Lesson.lesson_date == today,
                Lesson.completed == True
            )
            .scalar()
        )

        # Tính toán doanh thu dựa trên target_month và target_year đã xử lý
        monthly_revenue = (
            db.query(
                func.coalesce(
                    func.sum(Student.session_fee),
                    0
                )
            )
            .join(
                Lesson,
                Lesson.student_id == Student.id
            )
            .filter(
                func.extract(
                    "month",
                    Lesson.lesson_date
                ) == target_month,  # Thay đổi ở đây

                func.extract(
                    "year",
                    Lesson.lesson_date
                ) == target_year,   # Thay đổi ở đây

                Lesson.completed == True
            )
            .scalar()
        )

        students = (
            db.query(Student)
            .filter(Student.active == True)
            .all()
        )

        low_balance = 0
        out_of_sessions = 0

        for student in students:
            remaining = (
                StudentService
                .get_remaining_sessions(
                    db,
                    student.id
                )["remaining"]
            )

            if 0 < remaining <= 3:
                low_balance += 1
            elif remaining <= 0:
                out_of_sessions += 1

        return {
            "total_students": total_students,
            "today_classes": today_classes,
            "today_revenue": float(today_revenue),
            "monthly_revenue": float(monthly_revenue),
            "low_balance_students": low_balance,
            "out_of_sessions_students": out_of_sessions
        }