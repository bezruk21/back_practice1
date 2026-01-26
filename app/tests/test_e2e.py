import pytest


@pytest.mark.asyncio
async def test_complete_user_flow(ac):

    email = "happy_user@test.com"
    pwd = "secure_password"
    await ac.post("/register", json={"email": email, "password": pwd})


    login_res = await ac.post("/auth/login", json={"email": email, "password": pwd})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}


    animal_data = {"name": "Байрактар", "age": 2, "desc": "Бойовий кіт"}
    create_res = await ac.post("/animals", json=animal_data, headers=headers)
    assert create_res.status_code == 201


    list_res = await ac.get("/animals")
    assert len(list_res.json()) > 0
    assert list_res.json()[0]["name"] == "Байрактар"