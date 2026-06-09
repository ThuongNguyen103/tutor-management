from sqlalchemy.orm import Session

from app.models.tuition import TuitionPayment


class TuitionService:

    @staticmethod
    def get_all(db: Session):

        return (
            db.query(TuitionPayment)
            .order_by(
                TuitionPayment.payment_date.desc()
            )
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        tuition_id: int
    ):

        return (
            db.query(TuitionPayment)
            .filter(
                TuitionPayment.id == tuition_id
            )
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        payload
    ):

        tuition = TuitionPayment(
            student_id=payload.student_id,
            sessions_added=payload.sessions_added,
            amount=payload.amount,
            payment_date=payload.payment_date,
            note=payload.note
        )

        db.add(tuition)

        db.commit()

        db.refresh(tuition)

        return tuition

    @staticmethod
    def delete(
        db: Session,
        tuition
    ):

        db.delete(tuition)

        db.commit()

    @staticmethod
    def update(
        db: Session,
        tuition,
        payload
    ):

        tuition.sessions_added = payload.sessions_added
        tuition.amount = payload.amount
        tuition.payment_date = payload.payment_date
        tuition.note = payload.note

        db.commit()

        db.refresh(tuition)

        return tuition
    
    @staticmethod
    def get_by_student(
        db: Session,
        student_id: int
    ):

        return (
            db.query(TuitionPayment)
            .filter(
                TuitionPayment.student_id == student_id
            )
            .order_by(
                TuitionPayment.payment_date.desc()
            )
            .all()
        )