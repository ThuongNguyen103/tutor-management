from datetime import date, datetime

from sqlalchemy.orm import Session

from app.models.schedule import Schedule


class ScheduleService:
    @staticmethod
    def get_all(db: Session):

        return (
            db.query(Schedule)
            .order_by(
                Schedule.day_of_week,
                Schedule.start_time
            )
            .all()
        )
    
    @staticmethod
    def get_by_id(
        db: Session,
        schedule_id: int
    ):

        return (
            db.query(Schedule)
            .filter(
                Schedule.id == schedule_id
            )
            .first()
        )
    
    @staticmethod
    def create(
        db: Session,
        payload
    ):

        schedule = Schedule(
            student_id=payload.student_id,
            day_of_week=payload.day_of_week,
            start_time=payload.start_time,
            end_time=payload.end_time
        )

        db.add(schedule)

        db.commit()

        db.refresh(schedule)

        return schedule
    
    @staticmethod
    def update(
        db: Session,
        schedule,
        payload
    ):

        schedule.day_of_week = payload.day_of_week
        schedule.start_time = payload.start_time
        schedule.end_time = payload.end_time
        schedule.active = payload.active

        db.commit()

        db.refresh(schedule)

        return schedule
    
    @staticmethod
    def delete(
        db: Session,
        schedule
    ):

        db.delete(schedule)

        db.commit()

    @staticmethod
    def get_today(
        db: Session
    ):

        today = datetime.now().isoweekday()

        return (
            db.query(Schedule)
            .filter(
                Schedule.day_of_week == today,
                Schedule.active == True
            )
            .order_by(
                Schedule.start_time
            )
            .all()
        )
    
    @staticmethod
    def get_by_date(
        db: Session,
        lesson_date: date
    ):

        weekday = lesson_date.isoweekday()

        return (
            db.query(Schedule)
            .filter(
                Schedule.day_of_week == weekday,
                Schedule.active == True
            )
            .order_by(
                Schedule.start_time
            )
            .all()
        )
    
    @staticmethod
    def get_week_schedule(
        db: Session
    ):

        result = {}

        for day in range(1, 8):

            schedules = (
                db.query(Schedule)
                .filter(
                    Schedule.day_of_week == day,
                    Schedule.active == True
                )
                .order_by(
                    Schedule.start_time
                )
                .all()
            )

            result[day] = schedules

        return result
    
    @staticmethod
    def check_conflict(
        db: Session,
        payload
    ):
        schedules = (
            db.query(Schedule)
            .filter(
                Schedule.day_of_week == payload.day_of_week,
                Schedule.active == True
            )
            .all()
        )

        for item in schedules:
            overlap = (
                payload.start_time < item.end_time
                and
                payload.end_time > item.start_time
            )

            if (
                overlap
                and
                item.student_id != payload.student_id
            ):
                return True
            return True

        return False
    
    @staticmethod
    def today_summary(
            db: Session
        ):
            schedules = ScheduleService.get_today(db)

            return {
                "total_classes": len(schedules),
                "classes": schedules
            }

    @staticmethod
    def get_by_student(
        db: Session,
        student_id: int
    ):

        return (
            db.query(Schedule)
            .filter(
                Schedule.student_id == student_id
            )
            .order_by(
                Schedule.day_of_week,
                Schedule.start_time
            )
            .all()
        )