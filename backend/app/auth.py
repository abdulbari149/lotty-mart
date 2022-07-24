import email
import json
from flask import Blueprint, redirect, render_template, request
from secrets import token_hex
from app.repository.user_repository import user_repo
from app.base import BaseService
from models.users import User
from cryptography.fernet import Fernet

class AuthService(BaseService):
    def __init__(self):
        super().__init__("auth")
        self.user_repo = user_repo
    
    def register_routes(self):
        @self.app.route("/auth/login", methods=["POST"])
        def login():
            try:
                data = request.get_json()
                if "email" not in data or data["email"] == "" or data["email"] == None :
                    raise Exception("Email is required")
                if "password" not in data or data["password"] == "" or data["password"] == None:
                    raise Exception("password is required")
                
                current_user = None
                users = self.user_repo.get()
                for user in users: 
                    if user['email'] == data['email']:
                        current_user = user
                        break
                else:
                    raise Exception("A user with the email not found")
                print(current_user)
                user = User(current_user["id"], current_user["first_name"], current_user["last_name"], current_user["email"], current_user["password"], current_user["role"], current_user["address"] ,hash_key=current_user["hash_key"], created_at = current_user["created_at"], updated_at =current_user["updated_at"])
                password = user.decrypt_password() 
                if data["password"] != password:
                    raise Exception("Password is incorrect")
                self.data = user.get_info()    
                self.message = "You are logged in"
                self.error = False
                self.status = 200
            except Exception as err:
                self.error = True
                self.message = str(err)
                self.data = None
                self.status = 404
            finally:
                self.response = { "data": self.data, "message": self.message, "error": self.error }
                return self.response, self.status, self.headers
        
        @self.app.route("/auth/register", methods=["POST"])
        def register():
            try:
                data = request.get_json()
                if "first_name" not in data or data["first_name"] == "" or data["first_name"] == None :
                    raise Exception("First Name is required")
                if "last_name" not in data or data["last_name"] == "" or data["last_name"] == None :
                    raise Exception("Last Name is required")
                if "role" not in data or data["role"] == "" or data["role"] == None:
                    raise Exception("Role is required")
                if data["role"] not in ("customer", "admin"):
                    raise Exception("Role value is wrong")
                if "address" not in data or data["address"] == "" or data["address"] == None :
                    raise Exception("Address is required")
                if "email" not in data or data["email"] == "" or data["email"] == None :
                    raise Exception("Email is required")
                if "password" not in data or data["password"] == "" or data["password"] == None:
                    raise Exception("password is required")
                
                current_user = None
                users = self.user_repo.get()
                for user in users: 
                    if user['email'] == data['email']:
                        current_user = user
                        break
                if current_user != None:
                    raise Exception("A user already exists with the provided email address")
                hash_key = Fernet.generate_key()
                user = User(users[-1]["id"] + 1,data["first_name"], data["last_name"], data["email"], data["password"], data["role"], data["address"], hash_key=hash_key.decode())
                user.encrypt_password()     
                result = self.user_repo.add({**user.get_info(), "password": user.password, "hash_key": user.hash_key})
                if result != True:
                    raise Exception("An error occured while adding the user")
                self.data = user.get_info()    
                self.message = "Your account was registered successfully"
                self.error = False
                self.status = 200
            except Exception as err:
                self.error = True
                self.message = str(err)
                self.data = None
                self.status = 404
            finally:
                self.response = { "data": self.data, "message": self.message, "error": self.error }
                return self.response, self.status, self.headers
            

            #         if(user["password"] == data["password"] and user["email"] == data["email"]):
            #             token = token_hex(16)
            #             token_file = open("data/token.txt", "a+")
            #             token_file.write(f"{token}\n")
            #             token_file.close()
            #             return json.dumps({ "data": user, "token": token }), 200
            #     else:
            #         return json.dumps({ "message":  "user wasn't found" }), 404
            