from abc import ABC, abstractmethod
from flask import Blueprint
from app.repository.abstract_repository import BaseRepository
from app.repository.cart_repository import CartRepository
from app.repository.product_repository import ProductRepository


class BaseService(ABC):
    def __init__(self, name: str):
        self.data = None
        self.message = ""
        self.error = None
        self.status = 0
        self.response = {}
        self.headers = {"Content-type": "application/json"}
        self.app = Blueprint(name, __name__, template_folder="templates")
        self.register_routes()
    @abstractmethod
    def register_routes(self):
        pass