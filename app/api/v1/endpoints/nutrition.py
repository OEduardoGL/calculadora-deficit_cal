from fastapi import APIRouter
from app.schemas.nutrition import UserInput, NutritionResponse
from app.services.nutrition import calcular_nutricao

router = APIRouter(tags=["nutrition"])

@router.post("/nutrition/calculate", response_model=NutritionResponse)
def calculate(data: UserInput):
    return calcular_nutricao(data)
