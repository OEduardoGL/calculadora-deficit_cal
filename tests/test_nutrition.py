import httpx
import pytest
from fastapi import status

from app.main import app


@pytest.mark.asyncio
async def test_calculate_basic():
    payload = {
        "sexo": "M",
        "peso": 80,
        "altura": 180,
        "idade": 28,
        "fator_atividade": "moderadamente_ativo",
        "objetivo": "perder_gordura",
    }
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/api/v1/nutrition/calculate", json=payload)
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "tmb" in data and "gcd" in data and "macros_meta" in data
    assert data["faixa_calorias"][0] < data["faixa_calorias"][1]
