from pydantic import BaseModel
from app.schemas.nutrition import UserInput, NutritionResponse

class CalculationCreate(BaseModel):
    input: UserInput
    output: NutritionResponse

class CalculationOut(BaseModel):
    id: int
    input: UserInput
    output: NutritionResponse
