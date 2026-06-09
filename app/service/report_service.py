from requests import Session
from sqlalchemy import func

from app.models.tuition import TuitionPayment
from app.models.lesson import Lesson

class ReportService:

    @staticmethod
    def monthly_revenue(
        db: Session,
        year: int,
        month: int
    ):

        revenue = (
            db.query(
                func.coalesce(
                    func.sum(
                        TuitionPayment.amount
                    ),
                    0
                )
            )
            .filter(
                func.extract(
                    "month",
                    TuitionPayment.payment_date
                ) == month,
                func.extract(
                    "year",
                    TuitionPayment.payment_date
                ) == year
            )
            .scalar()
        )

        return {
            "year": year,
            "month": month,
            "revenue": float(revenue)
        }
    
    @staticmethod
    def monthly_lessons(
        db: Session,
        year: int,
        month: int
    ):

        count = (
            db.query(Lesson)
            .filter(
                func.extract(
                    "month",
                    Lesson.lesson_date
                ) == month,
                func.extract(
                    "year",
                    Lesson.lesson_date
                ) == year
            )
            .count()
        )

        return {
            "year": year,
            "month": month,
            "lessons": count
        }