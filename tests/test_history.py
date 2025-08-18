import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app
from uuid import uuid4

def find_numeric_value(obj, keys_lower):
    """Busca recursiva em dict/list por qualquer chave em keys_lower com valor numérico."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() in keys_lower and isinstance(v, (int, float)):
                return v
            found = find_numeric_value(v, keys_lower)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for el in obj:
            found = find_numeric_value(el, keys_lower)
            if found is not None:
                return found
    return None

@pytest.mark.asyncio
async def test_save_and_history_flow(client: AsyncClient):
    # cria usuário e login (email único por execução)
    email = f"h{uuid4().hex[:6]}@example.com"
    password = "123456"

    await client.post("/api/v1/auth/register", json={"email": email, "password": password})
    r = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r.status_code == status.HTTP_200_OK
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # salva um cálculo
    payload = {
        "sexo": "M",
        "peso": 80,
        "altura": 180,
        "idade": 28,
        "fator_atividade": "moderadamente_ativo",
        "objetivo": "perder_gordura",
    }
    r = await client.post("/api/v1/nutrition/save", json=payload, headers=headers)
    assert r.status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED)

    # consulta histórico
    r = await client.get("/api/v1/nutrition/history", headers=headers)
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert isinstance(data, list) and len(data) >= 1

    item = data[0]

    assert "id" in item
    assert "input" in item and isinstance(item["input"], dict)
    assert item["input"].get("objetivo") == payload["objetivo"]

    keys = {"gcd", "tdee", "calorias", "tmb"}
    gcd_value = find_numeric_value(item, keys)

    if gcd_value is None and isinstance(item.get("faixa_calorias"), list) and len(item["faixa_calorias"]) == 2:
        low, high = item["faixa_calorias"]
        if isinstance(low, (int, float)) and isinstance(high, (int, float)):
            gcd_value = (low + high) / 2

    assert isinstance(gcd_value, (int, float)) and gcd_value > 0, f"Não encontrei {keys} ou faixa_calorias numéricas em: {item}"
