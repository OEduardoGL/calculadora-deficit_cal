from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Definindo os níveis de atividade
FACTOR_ACTIVITY = {
    "sedentario": 1.2,
    "levemente_ativo": 1.375,
    "moderadamente_ativo": 1.55,
    "muito_ativo": 1.725,
    "extremamente_ativo": 1.9
}

class UserInput(BaseModel):
    sexo: str  # "M" ou "F"
    peso: float
    altura: float
    idade: int
    fator_atividade: str  # "sedentario", "levemente_ativo", "moderadamente_ativo", "muito_ativo", "extremamente_ativo"
    objetivo: str  # "perder_gordura" ou "ganhar_massa"

@app.post("/calcular")
def calcular_dieta(data: UserInput):
    # Cálculo do TMB (Mifflin-St Jeor)
    if data.sexo == "M":
        tmb = 10 * data.peso + 6.25 * data.altura - 5 * data.idade + 5
    else:
        tmb = 10 * data.peso + 6.25 * data.altura - 5 * data.idade - 161

    # Gasto Calórico Diário (GCD)
    fator = FACTOR_ACTIVITY[data.fator_atividade]
    gcd = tmb * fator

    # Objetivo de calorias baseado no objetivo
    if data.objetivo == "perder_gordura":
        meta_calorias = gcd - 500
        cal_minima = gcd - 700  # Margem saudável mínima para perder gordura
        cal_maxima = gcd - 300  # Margem saudável máxima para perder gordura
    else:  # Ganho de massa magra
        meta_calorias = gcd + 300
        cal_minima = gcd + 200  # Margem saudável mínima para ganho de massa magra
        cal_maxima = gcd + 500  # Margem saudável máxima para ganho de massa magra

    # Distribuição dos macronutrientes
    proteina = data.peso * 2  # Proteína 2x por kg de peso
    gordura = data.peso * 1  # Gordura 1g por kg de peso
    
    # Para o cálculo de carboidratos (calorias restantes)
    def calcular_macros(calorias):
        carbo = (calorias - (proteina * 4 + gordura * 9)) / 4
        return {
            "Proteínas (g)": proteina,
            "Gorduras (g)": gordura,
            "Carboidratos (g)": carbo,
        }
    
    # Distribuições para os 3 casos
    macros_minimo = calcular_macros(cal_minima)
    macros_maximo = calcular_macros(cal_maxima)
    macros_meta = calcular_macros(meta_calorias)

    return {
        "TMB": round(tmb, 2),
        "GCD": round(gcd, 2),
        "Meta Calorias": round(meta_calorias, 2),
        "Calorias Mínimas": round(cal_minima, 2),
        "Calorias Máximas": round(cal_maxima, 2),
        "Macronutrientes (Mínimo)": macros_minimo,
        "Macronutrientes (Máximo)": macros_maximo,
        "Macronutrientes (Meta)": macros_meta,
    }
