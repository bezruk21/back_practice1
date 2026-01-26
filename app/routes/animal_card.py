from typing import List
from fastapi import APIRouter, HTTPException, Response
from beanie import PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from starlette import status
from starlette.responses import StreamingResponse

from app.models.animal_card import AnimalCardOut, AnimalCard, AnimalCardUpdate
from app.models.user import User, UserOut, UserUpdate
from app.util.storage import save_file_to_db

router = APIRouter(prefix="/animals", tags=["Animals"])

@router.get("", response_model=List[AnimalCardOut])
async def get_all_animal_cards() -> List[AnimalCardOut]:
    return await AnimalCard.find_all().to_list()


@router.get("/{animal_card_id}", response_model=AnimalCardOut)
async def get_animal_card_by_id(animal_card_id: PydanticObjectId):
    animal_card = await AnimalCard.get(animal_card_id)
    if not animal_card:
        raise HTTPException(status_code=404, detail="Animal card not found")
    return animal_card


@router.post("", response_model=AnimalCardOut, status_code=201)
async def create_animal_card(card_data: AnimalCardUpdate):
    new_card = AnimalCard(**card_data.model_dump())
    await new_card.insert()
    return new_card
@router.patch("/{animal_card_id}", response_model=AnimalCardOut)
async def update_animal_card(
        animal_card_id: PydanticObjectId,
        update_data: AnimalCardUpdate
):
    animal_card = await AnimalCard.get(animal_card_id)
    if not animal_card:
        raise HTTPException(status_code=404, detail="Animal card not found")

    update_dict = update_data.model_dump(exclude_unset=True)

    await animal_card.set(update_dict)

    return animal_card

@router.delete("/{animal_card_id}")
async def delete_animal_card(animal_card_id: PydanticObjectId) -> Response:
    animal_card = await AnimalCard.get(animal_card_id)
    if not animal_card:
        raise HTTPException(status_code=404, detail="Animal card not found")

    await animal_card.delete()
    return Response(status_code=204)

from fastapi import Request, File, UploadFile


@router.post("/{animal_card_id}/upload-photo")
async def upload_photo(
        animal_card_id: PydanticObjectId,
        request: Request,
        file: UploadFile = File(...)
):
    animal_card = await AnimalCard.get(animal_card_id)

    if not animal_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Animal card with id {animal_card_id} not found"
        )

    db = request.app.db

    try:
        file_id = await save_file_to_db(db, file)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error saving file: {str(e)}"
        )

    animal_card.image = file_id
    await animal_card.save()

    return {"file_id": str(file_id), "status": "photo uploaded successfully"}

@router.get("/photo/{file_id}")
async def get_photo(file_id: PydanticObjectId,request: Request):
    db = request.app.db
    fs = AsyncIOMotorGridFSBucket(db)
    try:
        grid_out = await fs.open_download_stream(file_id)
        return StreamingResponse(grid_out, media_type=grid_out.metadata["content_type"])
    except Exception:
        raise HTTPException(status_code=404, detail="Фото не знайдено")