from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

# if settings.MODE == "TEST":
#     DATABASE_URL = f"postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASSWORD}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
#     DATABASE_PARAMS = {"poolclass": NullPool}
# else:
#     DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
#     DATABASE_PARAMS = {}

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    # to fix RuntimeError: Task <Task pending name='Task-4'
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

async_engine = create_async_engine(DATABASE_URL, echo=True, **DATABASE_PARAMS)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


class Base(DeclarativeBase): ...


async def get_session():
    async with async_session() as session:
        yield session


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
