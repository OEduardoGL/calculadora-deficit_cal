from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.repositories import calculation_repo
from app.schemas.nutrition import NutritionResponse, UserInput
from app.services.nutrition import calcular_nutricao

router = APIRouter(tags=["nutrition"])


@router.post("/nutrition/calculate", response_model=NutritionResponse)
def calculate(data: UserInput):
    return calcular_nutricao(data)


@router.post("/nutrition/save", response_model=dict)
def save_history(
    payload: UserInput, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    result = calcular_nutricao(payload)
    calculation_repo.create(
        db,
        user_id=user.id,
        payload=payload.model_dump(),
        result=result,
        objetivo=payload.objetivo.value,
        gcd=result["gcd"],
    )
    return {"status": "ok"}


@router.get("/nutrition/history")
def list_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    items = calculation_repo.list_by_user(db, user_id=user.id, skip=skip, limit=limit)
    return [
        {
            "id": c.id,
            "input": c.payload,
            "output": c.result,
        }
        for c in items
    ]
