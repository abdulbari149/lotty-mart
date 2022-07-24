from dataclasses import dataclass
from datetime import date
from math import prod
from operator import le
from models.base import BaseModel
from models.product import Product

class CartItem(BaseModel):
    id: str | int
    product_id:str | int
    ordered_quantity:int
    price_per_unit:int
    total_amount:int
    created_at: date
    updated_at: date
    def __init__(self, id, product_id, ordered_quantity, price_per_unit, created_at = None, updated_at = None):
        super().__init__(id, created_at, updated_at)
        self.product_id = product_id
        self.ordered_quantity = ordered_quantity
        self.price_per_unit = price_per_unit
        self.total_amount =  self.price_per_unit * self.ordered_quantity

    def update_quantity(self, quantity):
        self.ordered_quantity = quantity
        self.total_amount = self.price_per_unit * quantity
    
    def get_info(self):
        return { "id": self.id, "product_id": self.product_id, "ordered_quantity": self.ordered_quantity, "price_per_unit": self.price_per_unit, "total_amount": self.total_amount}

# items = [{ "id": 2, "price_per_uni" }]

class Cart(BaseModel):
    id: str | int
    user_id:int
    total_price: float
    items_count: int 
    items: list[CartItem | None] 
    promo_code: str | None 
    def __init__(self,id,user_id, items = []):
        # super(
        self.id = id
        self.user_id = user_id
        self.items_count = len(items)
        self.promo_code = ""
        self.set_cart_items(items)
        self.calculate_total_price()
    
    def set_cart_items(self, items):
        new_items = []
        if len(items) > 0:
            for item in items:
                new_items.append(CartItem(item["id"], item["product_id"], item["ordered_quantity"], item["price_per_unit"]))
        self.items = new_items    
    def calculate_total_price(self):
        self.total_price = 0
        if len(self.items) == 0:
            return
        for item in self.items:
            self.total_price += item.total_amount

    def add_cart_item(self, product_id, ordered_quantity, price_per_unit): 
        new_item_id = self.items_count + 1
        new_cart_item = CartItem(id=new_item_id, product_id=product_id, ordered_quantity=ordered_quantity, price_per_unit=price_per_unit)
        self.items.append(new_cart_item)
        self.items_count = len(self.items)
        self.calculate_total_price()
    
    def remove_cart_item(self, cart_item_id):
        items = []
        for item in self.items:
            if item.id != cart_item_id:
                items.append(item)
        self.items = items
        self.items_count = len(items)
        self.calculate_total_price()       

    def updated_units(self, cart_item_id: int, units: int):
        for item in self.items:
            if item.id == cart_item_id:
                item.update_quantity(units)
        self.calculate_total_price()
        
        
    def get_info(self):
        items_info = []
        for item in self.items:
            items_info.append(item.get_info())
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": items_info,
            "items_count": self.items_count,
            'total_price': self.total_price,
            "promo_code": self.promo_code
        }