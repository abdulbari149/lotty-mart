from typing import Any
from app.repository.abstract_repository import BaseRepository
from models.cart import Cart
class CartRepository(BaseRepository):
    def __init__(self):
        super().__init__(name="cart")
        
    def get(self, id: str | None = None):
        return super().get(id)
    def add(self, data):
        return super().add(data)
    def delete(self, id: str | None = None):
        return super().delete(id)
    def update(self, data, id: int):
        return super().update(data, id)
    def get_by_user_id(self, user_id):
        return super().get(user_id, "user_id")
    def initiate_cart(self, user_id):
        carts_count = self.get()[-1]["id"]
        new_cart = Cart(id=carts_count + 1,user_id=user_id)
        new_cart_info = new_cart.get_info()
        result = self.add(data=new_cart_info)
        if result != True:
            raise Exception(result)
        return new_cart_info

cart_repo = CartRepository()