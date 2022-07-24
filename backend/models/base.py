from abc import ABC, abstractmethod
from datetime import datetime
class BaseModel(ABC): 
    def __init__(self, id, created_at = None, updated_at = None):
        self.id = id
        self.created_at = self.create_date() if created_at == None else created_at 
        self.updated_at = self.create_date() if updated_at == None else updated_at 
    @abstractmethod
    def get_info(self):
        pass
    
    @staticmethod
    def create_date():
        return datetime.now().isoformat()

            