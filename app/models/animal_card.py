from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Indexed, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field
class AnimalCardUpdate(BaseModel):
    """Updatable animal card fields."""

    # Information about animal
    name: str | None = None
    age: int | None= None
    desc: str | None = None
    image: PydanticObjectId | None = None
class AnimalCardOut(BaseModel):
    """Animal fields returned to the client."""

    # Information about animal
    id: PydanticObjectId = Field(alias="_id")
    name: str | None = None
    age: int  | None = None
    desc: str | None = None
    image: PydanticObjectId | None = None

    class Config:
        populate_by_name = True
class AnimalCard(Document,AnimalCardOut):
    """Animal fields returned to the client."""

    # Information about animal
    name: str | None = None
    age: int | None= None
    desc: str | None = None
    image: PydanticObjectId | None = None
    @property
    def created_at(self) -> datetime | None:
        """Date of creation of the animal card."""
        return self.id.generation_time if self.id else None