from abc import ABC, ABCMeta, abstractclassmethod, abstractmethod
from cmath import inf
from ctypes import Union
from dataclasses import dataclass
from datetime import date
from itertools import product
import os
from models.base import BaseModel
@dataclass
class Clothes:
    size: str
    color: str
    cloth_type: str
    
@dataclass
class Food:
    ingredients: list[str]
    flavour: str
    weight: int 
    raw:bool =False

@dataclass
class ElectronicItem:
    type:str
    compatibility:str
    color:str
    
class Product(BaseModel):
    id: int
    make:str
    name: str
    price: float
    created_at : date
    updated_at: date
    category: str
    image_url: str
    brand_name: str
    warranty:   str
    packaging_type:str
    shipping_fare:str
    units:int
    details: Clothes | Food | ElectronicItem    
    def __init__(self, id, name, price, description ,make, category, image_name,brand_name, warranty, packaging_type, shipping_fare, units, details, created_at=None, updated_at=None):
        super().__init__(id, created_at=created_at, updated_at=updated_at)
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.image_url = f"{os.environ.get('BASE_URL')}/images/{image_name}"
        self.brand_name = brand_name
        self.make = make
        self.warranty = warranty
        self.packaging_type = packaging_type
        self.shipping_fare = shipping_fare
        self.units = units
        self.details = self.create_details(details)
    def get_detail_items(self, details, *args):
        values = []
        for arg in args:
            if arg in details.keys():
                values.append(details[arg])
            else:
                values.append(None)
        return values      
                
    def create_details(self, details):
        if self.category == "clothes":
            size, color, cloth_type = self.get_detail_items(details, "size", "color", "cloth_type")
            return Clothes(size, color,cloth_type )
        elif self.category == "food":
            ingredients, flavour, weight, raw = self.get_detail_items(details, "ingredients", "flavour", "weight", "raw")
            return Food(ingredients, flavour, weight, raw)
        elif self.category == "electronic_devices" :
            item_type, compatibility, color = self.get_detail_items(details, "type", "compatibility", "color")
            return ElectronicItem(item_type, compatibility, color)
        else:
            print("Else Runs")
    
    def get_info(self):
        info = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "make": self.make,
            "category": self.category, 
            "brand_name": self.brand_name, 
            "warranty" : self.warranty,
            "image_url": self.image_url,
            "packaging_type": self.packaging_type,
            "shipping_fare": self.shipping_fare,
            "units": self.units,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        if isinstance(self.details, ElectronicItem):
            info["type"] = self.details.type
            info["color"] = self.details.color
            info["compatibility"] = self.details.compatibility
        
        elif isinstance(self.details, Food):
            info["ingredients"] = self.details.ingredients
            info["raw"] = self.details.raw
            info["flavour"] = self.details.flavour
            info["weight"] = self.details.weight
            
        elif isinstance(self.details, Clothes):
            info["size"] = self.details.size
            info["color"] = self.details.color
            info["cloth_type"] = self.details.cloth_type
        return info