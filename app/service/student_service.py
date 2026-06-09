from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.student import Student
from sqlalchemy import func
from app.models.lesson import Lesson
from app.models.tuition import TuitionPayment
from app.models.schedule import Schedule


class StudentService:

    @staticmethod
    def get_all(
        db: Session,
        keyword: str | None = None
    ):

        query = (
            db.query(Student)
            .filter(Student.active == True)
        )

        if keyword:
            query = query.filter(
                Student.full_name.ilike(
                    f"%{keyword}%"
                )
            )

        return (
            query
            .order_by(Student.id.desc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        student_id: int
    ):

        return (
            db.query(Student)
            .filter(Student.id == student_id)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        payload
    ):

        student = Student(
            full_name=payload.full_name,
            parent_name=payload.parent_name,
            parent_phone=payload.parent_phone,
            note=payload.note,
            session_fee=payload.session_fee
        )

        db.add(student)

        db.commit()

        db.refresh(student)

        return student

    @staticmethod
    def update(
        db: Session,
        student,
        payload
    ):

        student.full_name = payload.full_name
        student.parent_name = payload.parent_name
        student.parent_phone = payload.parent_phone
        student.note = payload.note
        student.session_fee = payload.session_fee
        student.active = payload.active

        db.commit()

        db.refresh(student)

        return student

    @staticmethod
    def delete(
        db: Session,
        student
    ):

        student.active = False

        db.commit()

        return True
    
    @staticmethod
    def get_remaining_sessions(
        db: Session,
        student_id: int
    ):

        purchased = (
            db.query(
                func.coalesce(
                    func.sum(
                        TuitionPayment.sessions_added
                    ),
                    0
                )
            )
            .filter(
                TuitionPayment.student_id == student_id
            )
            .scalar()
        )

        studied = (
            db.query(
                func.count(
                    Lesson.id
                )
            )
            .filter(
                Lesson.student_id == student_id,
                Lesson.completed == True
            )
            .scalar()
        )

        return {
            "total_purchased": purchased,
            "total_studied": studied,
            "remaining": purchased - studied
        }
    

    @staticmethod
    def get_low_balance_students(
        db: Session,
        threshold: int = 3
    ):

        students = db.query(Student).all()

        result = []

        for student in students:

            remaining = StudentService.get_remaining_sessions(
                db,
                student.id
            )["remaining"]

            if remaining <= threshold:

                result.append({
                    "student_id": student.id,
                    "name": student.full_name,
                    "remaining": remaining
                })

        return result

    @staticmethod
    def get_student_lessons(
        db: Session,
        student_id: int
    ):

        return (
            db.query(Lesson)
            .filter(
                Lesson.student_id == student_id
            )
            .order_by(
                Lesson.lesson_date.desc()
            )
            .all()
        )

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

    @staticmethod
    def students_without_schedule(
        db: Session
    ):

        students = db.query(Student).all()

        result = []

        for student in students:

            has_schedule = (
                db.query(Schedule)
                .filter(
                    Schedule.student_id == student.id
                )
                .first()
            )

            if not has_schedule:

                result.append(student)

        return result

    @staticmethod
    def get_out_of_sessions_students(
        db: Session
    ):

        students = db.query(Student).all()

        result = []

        for student in students:

            remaining = (
                StudentService
                .get_remaining_sessions(
                    db,
                    student.id
                )["remaining"]
            )

            if remaining <= 0:

                result.append({
                    "id": student.id,
                    "full_name": student.full_name,
                    "remaining": remaining
                })

        return result