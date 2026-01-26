import pytest
from app.util.password import hash_password, verify_password
from app.models.user import UserAuth

def test_password_logic():
    pwd = "secret_password"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("wrong_pass", hashed) is False

def test_user_auth_schema():
    valid_user = UserAuth(email="test@me.com", password="123")
    assert str(valid_user.email) == "test@me.com"