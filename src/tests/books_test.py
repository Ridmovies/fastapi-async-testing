import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_books(client: AsyncClient):
    response = await client.get("/books")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_book(client: AsyncClient):
    response = await client.post("/books", json={"title": "test_title"})
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "test_title"


@pytest.mark.asyncio
async def test_get_book_by_id(client: AsyncClient):
    book_id = 1
    response = await client.get(f"/books/{book_id}")
    assert response.json()["id"] == 1
    assert response.json()["title"] == "test_title"

    book_id = 2
    response = await client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json() is None
