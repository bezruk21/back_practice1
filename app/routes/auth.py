from fastapi import APIRouter, HTTPException, Security
from fastapi_jwt import JwtAuthorizationCredentials

from app.models.auth import AccessToken, RefreshToken
from app.models.user import User, UserAuth
from app.jwt import access_security, refresh_security
from app.util.password import hash_password,verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login(user_auth: UserAuth) -> RefreshToken:
    print(f"DEBUG: Login attempt for email: {user_auth.email}")
    print(f"DEBUG: Password provided: {user_auth.password}")
    """Authenticate and returns the user's JWT."""
    user = await User.by_email(user_auth.email)
    if user is None:
        print("DEBUG: User NOT found in DB")
        raise HTTPException(status_code=401, detail="Bad email or password")

    print(f"DEBUG: User found! DB Password hash: {user.password}")

    is_valid = verify_password(user_auth.password, user.password)
    print(f"DEBUG: Password valid? {is_valid}")

    if not is_valid:
        print("DEBUG: Password mismatch")
        raise HTTPException(status_code=401, detail="Bad email or password")


    access_token = access_security.create_access_token(user.jwt_subject)
    refresh_token = refresh_security.create_refresh_token(user.jwt_subject)
    return RefreshToken(access_token=access_token, refresh_token=refresh_token)


