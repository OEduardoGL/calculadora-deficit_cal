from . import __name__ as _pkg  # noqa:F401 (apenas para namespace)
from typing import Dict, Tuple
from app.schemas.nutrition import UserInput, MacroDistribuicao, Objetivo, FatorAtividade

FACTORS: Dict[FatorAtividade, float] = {
    FatorAtividade.sedentario: 1.2,
    FatorAtividade.levemente_ativo: 1.375,
    FatorAtividade.moderadamente_ativo: 1.55,
    FatorAtividade.muito_ativo: 1.725,
    FatorAtividade.extremamente_ativo: 1.9,
}

def _tmb_mifflin(sexo: str, peso: float, altura_cm: float, idade: int) -> float:
    if sexo == "M":
        return 10 * peso + 6.25 * altura_cm - 5 * idade + 5
    return 10 * peso + 6.25 * altura_cm - 5 * idade - 161

def _target_calories(gcd: float, objetivo: Objetivo) -> Tuple[int, Tuple[int, int]]:
    if objetivo == Objetivo.perder_gordura:
        meta = gcd - 500
        faixa = (int(gcd - 700), int(gcd - 300))
    elif objetivo == Objetivo.ganhar_massa:
        meta = gcd + 300
        faixa = (int(gcd + 200), int(gcd + 500))
    else:  # manutenção / recomposição
        meta = gcd
        faixa = (int(gcd - 100), int(gcd + 100))
    return int(meta), faixa

def _macro_defaults(objetivo: Objetivo, peso: float) -> Tuple[float, float]:
    """
    Retorna (proteina_g, gordura_g) como defaults por kg.
    - cutting: prot 2.0 g/kg, gord 0.8 g/kg
    - manutenção/recomp: prot 1.8 g/kg, gord 0.9 g/kg
    - bulking limpo: prot 1.6 g/kg, gord 1.0 g/kg
    """
    if objetivo == Objetivo.perder_gordura:
        return 2.0 * peso, 0.8 * peso
    if objetivo == Objetivo.ganhar_massa:
        return 1.6 * peso, 1.0 * peso
    return 1.8 * peso, 0.9 * peso

def _macros_para_calorias(calorias: int, prot_g: float, gord_g: float) -> MacroDistribuicao:
    prot_kcal = prot_g * 4
    gord_kcal = gord_g * 9
    carb_kcal = max(calorias - (prot_kcal + gord_kcal), 0)
    carb_g = carb_kcal / 4
    return MacroDistribuicao(
        calorias=int(calorias),
        proteinas_g=round(prot_g, 1),
        gorduras_g=round(gord_g, 1),
        carboidratos_g=round(carb_g, 1),
    )

def calcular_nutricao(data: UserInput):
    tmb = _tmb_mifflin(data.sexo.value, data.peso, data.altura, data.idade)
    gcd = tmb * FACTORS[data.fator_atividade]
    meta_cal, faixa = _target_calories(gcd, data.objetivo)
    prot_g, gord_g = _macro_defaults(data.objetivo, data.peso)

    macros_meta = _macros_para_calorias(meta_cal, prot_g, gord_g)
    macros_min = _macros_para_calorias(faixa[0], prot_g, gord_g)
    macros_max = _macros_para_calorias(faixa[1], prot_g, gord_g)

    return {
        "tmb": int(round(tmb)),
        "gcd": int(round(gcd)),
        "objetivo_calorias": int(meta_cal),
        "faixa_calorias": (int(faixa[0]), int(faixa[1])),
        "macros_meta": macros_meta,
        "macros_min": macros_min,
        "macros_max": macros_max,
    }
