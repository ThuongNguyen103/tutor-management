from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.dependencies import get_db

from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse
)

from app.service.student_service import StudentService
from app.schemas.schedule import ScheduleResponse
from app.service.schedule_service import ScheduleService

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get(
    "",
    response_model=list[StudentResponse]
)
def get_students(
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):

    return StudentService.get_all(
        db,
        keyword
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = StudentService.get_by_id(
        db,
        student_id
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.post(
    "",
    response_model=StudentResponse,
    status_code=201
)
def create_student(
    payload: StudentCreate,
    db: Session = Depends(get_db)
):

    return StudentService.create(
        db,
        payload
    )


@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: Session = Depends(get_db)
):

    student = StudentService.get_by_id(
        db,
        student_id
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return StudentService.update(
        db,
        student,
        payload
    )


@router.delete(
    "/{student_id}"
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = StudentService.get_by_id(
        db,
        student_id
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    StudentService.delete(
        db,
        student
    )

    return {
        "message": "Student deleted"
    }

@router.get(
    "/{student_id}/remaining-sessions"
)
def remaining_sessions(
    student_id: int,
    db: Session = Depends(get_db)
):

    return StudentService.get_remaining_sessions(
        db,
        student_id
    )

@router.get(
    "/low-balance"
)
def low_balance_students(
    threshold: int = 3,
    db: Session = Depends(get_db)
):

    return (
        StudentService
        .get_low_balance_students(
            db,
            threshold
        )
    )

@router.get(
    "/{student_id}/lessons"
)
def get_student_lessons(
    student_id: int,
    db: Session = Depends(get_db)
):

    return StudentService.get_student_lessons(
        db,
        student_id
    )

@router.get(
    "/student/{student_id}",
    response_model=list[ScheduleResponse]
)
def get_student_schedule(
    student_id: int,
    db: Session = Depends(get_db)
):

    return ScheduleService.get_by_student(
        db,
        student_id
    )

@router.get(
    "/without-schedule"
)
def students_without_schedule(
    db: Session = Depends(get_db)
):

    return ScheduleService.students_without_schedule(
        db
    )

@router.get(
    "/out-of-sessions"
)
def out_of_sessions(
    db: Session = Depends(get_db)
):

    return (
        StudentService
        .get_out_of_sessions_students(
            db
        )
    )

