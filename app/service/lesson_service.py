from sqlalchemy.orm import Session

from app.models.lesson import Lesson


class LessonService:

    @staticmethod
    def get_all(db: Session):

        return (
            db.query(Lesson)
            .order_by(
                Lesson.lesson_date.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        lesson_id: int
    ):

        return (
            db.query(Lesson)
            .filter(
                Lesson.id == lesson_id
            )
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        payload
    ):

        lesson = Lesson(
            student_id=payload.student_id,
            lesson_date=payload.lesson_date,
            content=payload.content,
            completed=payload.completed
        )

        db.add(lesson)

        db.commit()

        db.refresh(lesson)

        return lesson

    @staticmethod
    def update(
        db: Session,
        lesson,
        payload
    ):

        lesson.lesson_date = payload.lesson_date
        lesson.content = payload.content
        lesson.completed = payload.completed

        db.commit()

        db.refresh(lesson)

        return lesson

    @staticmethod
    def delete(
        db: Session,
        lesson
    ):

        db.delete(lesson)

        db.commit()