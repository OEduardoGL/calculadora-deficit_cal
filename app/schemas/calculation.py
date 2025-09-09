from pydantic import BaseModel

from app.schemas.nutrition import NutritionResponse, UserInput


class CalculationCreate(BaseModel):
    input: UserInput
    output: NutritionResponse


class CalculationOut(BaseModel):
    id: int
    input: UserInput
    output: NutritionResponse
