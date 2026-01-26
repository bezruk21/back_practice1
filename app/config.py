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
    algorithm: str = config("ALGORITHM", default="HS256")
    access_token_expire_minutes: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)

    testing: bool = config("TESTING", default=False, cast=bool)


CONFIG = Settings()

SECRET_KEY = CONFIG.authjwt_secret_key
ALGORITHM = CONFIG.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = CONFIG.access_token_expire_minutes