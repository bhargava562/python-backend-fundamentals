from fastapi import FastAPI, HTTPException, status

from app.database import store
from app.schemas import ItemCreate, ItemRead, ItemUpdate


app = FastAPI(
    title="Day 18 FastAPI CRUD API",
    version="1.0.0",
    description="A simple CRUD API backed by an in-memory data store.",
)


@app.get("/", tags=["root"])
def root() -> dict[str, str]:
    return {"message": "Day 18 FastAPI CRUD API"}


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items", response_model=list[ItemRead], tags=["items"])
def list_items() -> list[dict[str, object]]:
    return store.list_items()


@app.get("/items/{item_id}", response_model=ItemRead, tags=["items"])
def get_item(item_id: int) -> dict[str, object]:
    item = store.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED, tags=["items"])
def create_item(payload: ItemCreate) -> dict[str, object]:
    return store.create_item(payload)


@app.put("/items/{item_id}", response_model=ItemRead, tags=["items"])
def update_item(item_id: int, payload: ItemUpdate) -> dict[str, object]:
    item = store.update_item(item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def delete_item(item_id: int) -> None:
    deleted = store.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
