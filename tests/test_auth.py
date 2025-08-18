import pytest
from httpx import AsyncClient
from fastapi import status
from uuid import uuid4

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    email = f"tester+{uuid4().hex[:6]}@example.com"
    password = "strongpass"

    # register
    r = await client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert r.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST)

    # login
    r = await client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert "access_token" in data and isinstance(data["access_token"], str) and data["access_token"]
