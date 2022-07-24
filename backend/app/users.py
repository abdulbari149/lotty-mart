import json
from app.base import BaseService
from app.repository.user_repository import user_repo

class UserService(BaseService):
    def __init__(self):
        super().__init__(name="users")
        self.user_repo = user_repo
        
    @staticmethod
    def checkUser(user_id = None):    
        if user_id == None:
            raise Exception("User Id is required")
        user = user_repo.get(int(user_id))
        if user == None:
            raise Exception("User doesn't exists")
        return user

   
    
    def register_routes(self):
        
        @self.app.route("/users/get", methods=["GET"])
        def get_users():
            try:
                self.data = self.user_repo.get()
                self.error = False
                self.message = "Users List"
                self.status = 200
            except:
                self.error = True
                self.message = "Error Occured"
                self.status = 500
                self.data = None
            finally:
                self.response = json.dumps({ "data": self.data, "error": self.error, "message": self.message })
                return self.response, self.status, self.headers
        @self.app.route("/users/get/<int:user_id>", methods=["GET"])
        def get_user_by_id(user_id):
            try:
                self.data = self.user_repo.get(int(user_id))
                self.error = False
                self.message = "Users Wih an id " + str(user_id)
                self.status = 200
            except:
                self.error = True
                self.message = "Error Occured"
                self.status = 500
                self.data = None
            finally:
                self.response = json.dumps({ "data": self.data, "error": self.error, "message": self.message })
                return self.response, self.status, self.headers
        
        