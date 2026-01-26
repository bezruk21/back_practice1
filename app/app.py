
from contextlib import asynccontextmanager

from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware

from app.config import CONFIG
from app.models.user import User

from app.routes.auth import router as AuthRouter
from app.routes.register import router as RegisterRouter
from app.routes.user import router as UserRouter




@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore
    """Initialize application services."""

    # type: ignore[attr-defined]
    app.db = AsyncIOMotorClient(CONFIG.mongo_uri).account

    # type: ignore[arg-type,attr-defined]
    await init_beanie(app.db, document_models=[User])
    print("Startup complete")
    yield
    print("Shutdown complete")


app = FastAPI(
    title="My Server",
    version="0.1.0",
    lifespan=lifespan,
)

#cors settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter)
app.include_router(RegisterRouter)
app.include_router(UserRouter)