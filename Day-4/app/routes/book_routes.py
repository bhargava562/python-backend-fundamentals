from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.models.book_models import Book, UpdateBook
from app.database.fake_db import books_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", status_code=200)
def get_books(
    author: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    results = books_db

    if author:
        results = [b for b in results if b["author"] == author]

    return results[skip : skip + limit]

@router.get("/{book_id}", status_code=200)
def get_book(book_id: int):
    if book_id < 0 or book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]

@router.post("/", status_code=201)
def create_book(book: Book):
    # check duplicate ISBN
    for b in books_db:
        if b["isbn"] == book.isbn:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")

    books_db.append(book.dict())
    return {"message": "Book created"}

@router.patch("/{book_id}", status_code=200)
def patch_book(book_id: int, book: UpdateBook):
    if book_id < 0 or book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")

    stored = books_db[book_id]
    update_data = book.dict(exclude_unset=True)
    stored.update(update_data)
    books_db[book_id] = stored

    return {"message": "Book partially updated"}

@router.put("/{book_id}", status_code=200)
def update_book(book_id: int, book: Book):
    if book_id < 0 or book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[book_id] = book.dict()
    return {"message": "Book updated"}

@router.delete("/{book_id}", status_code=200)
def delete_book(book_id: int):
    if book_id < 0 or book_id >= len(books_db):
        raise HTTPException(status_code=404, detail="Book not found")

    books_db.pop(book_id)
    return {"message": "Book deleted"}
