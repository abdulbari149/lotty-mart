from models.base import BaseModel
from cryptography.fernet import Fernet


class User(BaseModel):
    id: int
    first_name: str
    last_name:str
    email: str
    password: str
    hash_key: str
    role: str
    address: str
    
    def __init__(self, id, first_name, last_name, email, password, role, address, hash_key="", created_at = None, updated_at = None):
        super().__init__(id, created_at, updated_at)
        self.first_name = first_name    
        self.last_name = last_name
        self.email = email
        self.role = role
        self.address = address
        self.hash_key = hash_key
        self.password = password
        
    def encrypt_password(self):
        key = self.hash_key
        crypter = Fernet(key.encode())
        encrypted_password =crypter.encrypt(self.password.encode()).decode()
        self.password = encrypted_password
    def decrypt_password(self):
        key = self.hash_key
        pwd = self.password
        crypter = Fernet(key.encode())
        decrypted_password = crypter.decrypt(pwd.encode()).decode()
        print(pwd, decrypted_password) 
        return decrypted_password
    def get_info(self):
        info = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "address": self.address,
            "created_at": self.created_at,
            "updated_at": self.updated_at
            }
        return info