from typing import Any
from app.repository.abstract_repository import BaseRepository

class OrderRepository(BaseRepository):
    def __init__(self):
        super().__init__("order")
    def get(self, id: int | None = None, param="id"):
        return super().get(id, param)
    def add(self, data):
        return super().add(data)
    def update(self, data: Any, id: int):
        return super().update(data, id)
    def delete(self, id: str):
        return super().delete(id)
    def get_by_user_id(self, user_id: int):
        return super().get(user_id, "user_id")
order_repo = OrderRepository()