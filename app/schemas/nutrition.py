from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Sexo(str, Enum):
    M = "M"
    F = "F"


class FatorAtividade(str, Enum):
    sedentario = "sedentario"
    levemente_ativo = "levemente_ativo"
    moderadamente_ativo = "moderadamente_ativo"
    muito_ativo = "muito_ativo"
    extremamente_ativo = "extremamente_ativo"


class Objetivo(str, Enum):
    perder_gordura = "perder_gordura"
    manutencao_recomp = "manutencao_recomp"
    ganhar_massa = "ganhar_massa"


class UserInput(BaseModel):
    sexo: Sexo
    peso: float = Field(..., gt=20, lt=400, description="kg")
    altura: float = Field(..., gt=100, lt=250, description="cm")
    idade: int = Field(..., ge=14, le=90)
    fator_atividade: FatorAtividade
    objetivo: Objetivo

    @field_validator("peso")
    @classmethod
    def _peso(cls, v):
        return round(v, 2)


class MacroDistribuicao(BaseModel):
    calorias: int
    proteinas_g: float
    gorduras_g: float
    carboidratos_g: float


class NutritionResponse(BaseModel):
    tmb: int
    gcd: int
    objetivo_calorias: int
    faixa_calorias: tuple[int, int]
    macros_meta: MacroDistribuicao
    macros_min: MacroDistribuicao
    macros_max: MacroDistribuicao
