from fastapi import APIRouter, Body, HTTPException, Response
from datetime import datetime , timezone

from app.models.user import User, UserAuth, UserOut
from app.util.password import hash_password


router = APIRouter(prefix="/register", tags=["Register"])

embed = Body(..., embed=True)


@router.post("", response_model=UserOut)
async def user_registration(user_auth: UserAuth):  # type: ignore[no-untyped-def]
    """Create a new user."""
    user = await User.by_email(user_auth.email)
    if user is not None:
        raise HTTPException(409, "User with that email already exists")
    hashed = hash_password(user_auth.password)
    user = User(email=user_auth.email,
                password=hashed,
                email_confirmed_at=datetime.now(timezone.utc))

    await user.create()
    return user
