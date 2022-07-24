from typing import Any
from app.repository.abstract_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(name="users")
        
    def get(self, id: str | None = None):
        return super().get(id)
    def add(self, data):
        return super().add(data)
    def delete(self,  id: str | None = None):
        return super().delete(id)
    def update(self, data: Any, id: str | int):
        return super().update(data, int(id))
user_repo = UserRepository()