from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.lesson import (
    LessonCreate,
    LessonUpdate,
    LessonResponse
)

from app.service.lesson_service import (
    LessonService
)

router = APIRouter(
    prefix="/lessons",
    tags=["Lessons"]
)

@router.get(
    "",
    response_model=list[LessonResponse]
)
def get_lessons(
    db: Session = Depends(get_db)
):
    return LessonService.get_all(db)

@router.get(
    "/{lesson_id}",
    response_model=LessonResponse
)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):

    lesson = LessonService.get_by_id(
        db,
        lesson_id
    )

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return lesson

@router.post(
    "",
    response_model=LessonResponse
)
def create_lesson(
    payload: LessonCreate,
    db: Session = Depends(get_db)
):

    return LessonService.create(
        db,
        payload
    )

@router.put(
    "/{lesson_id}",
    response_model=LessonResponse
)
def update_lesson(
    lesson_id: int,
    payload: LessonUpdate,
    db: Session = Depends(get_db)
):

    lesson = LessonService.get_by_id(
        db,
        lesson_id
    )

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return LessonService.update(
        db,
        lesson,
        payload
    )

@router.delete(
    "/{lesson_id}"
)
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):

    lesson = LessonService.get_by_id(
        db,
        lesson_id
    )

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    LessonService.delete(
        db,
        lesson
    )

    return {
        "message": "Deleted"
    }