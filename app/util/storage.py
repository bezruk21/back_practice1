
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from beanie import PydanticObjectId
from fastapi import UploadFile


async def save_file_to_db(db, file: UploadFile) -> PydanticObjectId:
    fs = AsyncIOMotorGridFSBucket(db)

    file_id = await fs.upload_from_stream(
        file.filename,
        file.file,
        metadata={"content_type": file.content_type}
    )
    return file_id