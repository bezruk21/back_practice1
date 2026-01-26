from decouple import config
from pydantic import BaseModel,ConfigDict



class Settings(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    root_url: str = config("ROOT_URL")

    # Mongo Engine settings
    mongo_uri: str = config("MONGODB_URL")

    # Security settings
    authjwt_secret_key: str = config("JWT_SECRET_KEY")
    salt: bytes = config("SALT").encode()

    testing: bool = config("TESTING", default=False, cast=bool)


CONFIG = Settings()