from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, get_session, init_db


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


class BookInSchema(BaseModel):
    title: str


@app.get("/books")
async def get_all_books(session: AsyncSession = Depends(get_session)):
    stmt = select(Book)
    result: Result = await session.execute(stmt)
    return result.scalars().all()


@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Book).where(Book.id == book_id)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


@app.post("/books")
async def create_book(
    book_data: BookInSchema, session: AsyncSession = Depends(get_session)
):
    book = Book(**book_data.model_dump())
    session.add(book)
    await session.commit()
    return book
