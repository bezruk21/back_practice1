import pytest


@pytest.mark.asyncio
async def test_register_new_user(ac):
    payload = {"email": "new@example.com", "password": "password123"}
    response = await ac.post("/register", json=payload)

    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"


@pytest.mark.asyncio
async def test_login_fail_invalid_credentials(ac):
    payload = {"email": "not_exist@example.com", "password": "123"}
    response = await ac.post("/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Bad email or password"