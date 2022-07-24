from typing import Any
from app.repository.abstract_repository import BaseRepository
from models.product import Product

class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(name="product")
        
    def get(self, id: str | None = None):
        return super().get(id)
    def add(self, data):
        return super().add(data)
    def delete(self, id: str | None = None):
        return super().delete(id)
    def update(self, data: Any, id: str | int):
        return super().update(data, int(id))
product_repo = ProductRepository()