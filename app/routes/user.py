from typing import List
from fastapi import APIRouter, HTTPException, Response
from beanie import PydanticObjectId

from app.models.user import User, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserOut])
async def get_all_users():
    return await User.find_all().to_list()


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: PydanticObjectId):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: PydanticObjectId, update: UserUpdate):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    fields = update.model_dump(exclude_unset=True)

    if new_email := fields.pop("email", None):
        if new_email != user.email:
            existing_user = await User.by_email(new_email)
            if existing_user and existing_user.id != user.id:
                raise HTTPException(400, "Email already exists")
            user.email = new_email

    user = user.model_copy(update=fields)
    await user.save()
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: PydanticObjectId) -> Response:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return Response(status_code=204)