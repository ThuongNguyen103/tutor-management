from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.tuition import (
    TuitionCreate,
    TuitionUpdate,
    TuitionResponse
)

from app.service.tuition_service import (
    TuitionService
)

router = APIRouter(
    prefix="/tuitions",
    tags=["Tuitions"]
)

@router.get(
    "",
    response_model=list[TuitionResponse]
)
def get_tuitions(
    db: Session = Depends(get_db)
):
    return TuitionService.get_all(db)

@router.post(
    "",
    response_model=TuitionResponse
)
def create_tuition(
    payload: TuitionCreate,
    db: Session = Depends(get_db)
):

    return TuitionService.create(
        db,
        payload
    )

@router.get(
    "/{tuition_id}",
    response_model=TuitionResponse
)
def get_tuition(
    tuition_id: int,
    db: Session = Depends(get_db)
):

    tuition = TuitionService.get_by_id(
        db,
        tuition_id
    )

    if not tuition:
        raise HTTPException(
            status_code=404,
            detail="Tuition not found"
        )

    return tuition

@router.delete(
    "/{tuition_id}"
)
def delete_tuition(
    tuition_id: int,
    db: Session = Depends(get_db)
):

    tuition = TuitionService.get_by_id(
        db,
        tuition_id
    )

    if not tuition:
        raise HTTPException(
            status_code=404,
            detail="Tuition not found"
        )

    TuitionService.delete(
        db,
        tuition
    )

    return {
        "message": "Deleted"
    }

@router.put(
    "/{tuition_id}",
    response_model=TuitionResponse
)
def update_tuition(
    tuition_id: int,
    payload: TuitionUpdate,
    db: Session = Depends(get_db)
):

    tuition = TuitionService.get_by_id(
        db,
        tuition_id
    )

    if not tuition:
        raise HTTPException(
            status_code=404,
            detail="Tuition not found"
        )

    return TuitionService.update(
        db,
        tuition,
        payload
    )

@router.get(
    "/student/{student_id}",
    response_model=list[TuitionResponse]
)
def get_student_tuitions(
    student_id: int,
    db: Session = Depends(get_db)
):

    return TuitionService.get_by_student(
        db,
        student_id
    )