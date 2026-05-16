from __future__ import annotations

from itertools import count

from app.schemas import ItemCreate, ItemUpdate


class InMemoryItemStore:
    def __init__(self) -> None:
        self._items: dict[int, dict[str, object]] = {}
        self._ids = count(1)

    def list_items(self) -> list[dict[str, object]]:
        return list(self._items.values())

    def get_item(self, item_id: int) -> dict[str, object] | None:
        return self._items.get(item_id)

    def create_item(self, payload: ItemCreate) -> dict[str, object]:
        item_id = next(self._ids)
        item = {
            "id": item_id,
            "name": payload.name,
            "description": payload.description,
            "is_active": payload.is_active,
        }
        self._items[item_id] = item
        return item

    def update_item(self, item_id: int, payload: ItemUpdate) -> dict[str, object] | None:
        current = self._items.get(item_id)
        if current is None:
            return None

        if payload.name is not None:
            current["name"] = payload.name
        if payload.description is not None:
            current["description"] = payload.description
        if payload.is_active is not None:
            current["is_active"] = payload.is_active

        return current

    def delete_item(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None


store = InMemoryItemStore()
