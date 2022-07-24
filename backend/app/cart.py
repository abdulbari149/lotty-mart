import json
from math import prod
from tkinter.tix import Tree
from flask import Blueprint, redirect, request
from app.base import BaseService
from app.repository.cart_repository import cart_repo
from app.repository.user_repository import user_repo
from app.repository.product_repository import product_repo
from app.users import UserService
from models.cart import Cart, CartItem        

class CartService(BaseService):
    def __init__(self):
        super().__init__(name="cart")
        self.cart_repo = cart_repo   
        self.user_repo = user_repo
        self.product_repo = product_repo
        
    def register_routes(self):
        
        @self.app.route("/cart/get-items", methods=["GET"])
        def get_cart_items():
            try:
                user_id = request.args.get("user_id")
                user = UserService.checkUser(user_id)
                print(user)
                user_id = int(user["id"])
                cart = self.cart_repo.get_by_user_id(user_id)
                if cart == None:
                    self.data = self.cart_repo.initiate_cart(user_id)
                else:
                    cart_obj = Cart(cart["id"], cart["user_id"], cart['items'])
                    info = cart_obj.get_info()
                    cart_items = []
                    if len(cart_obj.items) > 0:
                        for item in cart_obj.items:
                            pid = item.product_id
                            product = self.product_repo.get(pid)
                            cart_item = item.get_info()
                            cart_item["product"] = product
                            cart_items.append(cart_item)
                        print(info["items"])
                        info["items"] = cart_items
                    self.data = info
                self.status = 200
                self.message = f"Cart for User {user_id}"
                self.error = False
            except Exception as err: 
                self.error = True
                self.message = str(err)
                self.data = None
                self.status = 404
            finally:
                self.response = json.dumps({ "data": self.data, "error": self.error, "message": self.message })
                return self.response, self.status, self.headers        
        
        @self.app.route("/cart/add-item", methods=["POST"])
        def add_cart_item():
            try:
                body = request.get_json()
                user_id  = body["user_id"] if "user_id" in body else None
                user = UserService.checkUser(user_id)
                user_id = int(user["id"])
                # Getting cart and creating an object
                cart_data = self.cart_repo.get_by_user_id(user_id=user_id)
                if cart_data == None:
                    cart_data = self.cart_repo.initiate_cart(user_id=user_id)
                cart = Cart(cart_data["id"], cart_data["user_id"], cart_data["items"])
                # Checking the product
                product_id = body["product_id"] if "product_id" in body else None
                units = body["units"] if "units" in body else None
                
                if product_id == None:
                    raise Exception("Product Id is a required field")
                if units == None:
                    raise Exception("Units is a required field")
                
                product = self.product_repo.get(int(product_id))
                if product == None:
                    raise Exception("Product wasn't found")
                if product["units"] == 0:
                    raise Exception("Sorry this product is out of stock")
                if product["units"] < units:
                    raise Exception("Units are too many")
            
                for item in cart.items:
                    print(item.product_id, product_id)
                    if item.product_id == product_id:
                        raise Exception("Product already Exists in the cart")   
                cart.add_cart_item(product_id=product_id, ordered_quantity=units, price_per_unit=product["price"])
                cart_info = cart.get_info()
                self.data = self.cart_repo.update(cart_info, cart.id)
                self.message = "Item has been added to the cart successfully"
                self.error = False
                self.status = 200
            except Exception as err: 
                self.error = True
                self.data = None
                self.message = str(err)
                self.status = 500
            finally:
                self.response = json.dumps({ "data": self.data, "error": self.error, "message": self.message })
                return self.response, self.status, self.headers
        
        @self.app.route("/cart/remove-item", methods=["DELETE"])
        def delete_item():
            try:
                body = request.get_json()
                user_id  = body["user_id"] if "user_id" in body else None
                user = UserService.checkUser(user_id)
                user_id = int(user["id"])
                cart_data = self.cart_repo.get_by_user_id(user_id=user_id)
                if cart_data == None:
                    raise Exception("Cart with the specified id wasn't found")
                cart = Cart(cart_data["id"], cart_data["user_id"], cart_data["items"])
                
                product_id = body["product_id"] if "product_id" in body else None
                cart_item_id = body["cart_item_id"] if "cart_item_id" in body else None
                
                if product_id == None:
                    raise Exception("Product Id is a required field")
                
                product = self.product_repo.get(int(product_id))
                if product == None:
                    raise Exception("Product wasn't found")
                
                for item in cart.items:
                    if item.product_id == product_id and item.id == cart_item_id:
                        break
                else: 
                    raise Exception("Product doesn't exists in the cart")
                cart.remove_cart_item(cart_item_id)
                new_cart = self.cart_repo.update(cart.get_info(), cart.id)
                self.data = {
                    "cartId":  new_cart["id"]
                }
                self.message = "Cart Item has been succesfully removed from the cart"
                self.error = True
                self.status = 200
            except Exception as err:
                self.error = True
                self.message = str(err)
                self.status = 500
                self.data = None
            finally:
                self.response = json.dumps({ "data": self.data, "message": self.message, "error": self.error })
                return self.response, self.status, self.headers
            
        
        
        @self.app.route("/cart/update-item", methods=["PUT"])
        def update_item():
            try:
                body = request.get_json()
                user_id  = body["user_id"] if "user_id" in body else None
                user = UserService.checkUser(user_id)
                
                user_id = int(user["id"])
                cart_data = self.cart_repo.get_by_user_id(user_id=user_id)
                if cart_data == None:
                    raise Exception("Cart with the specified id wasn't found")
                cart = Cart(cart_data["id"], cart_data["user_id"], cart_data["items"])
                
                product_id = body["product_id"] if "product_id" in body else None
                cart_item_id = body["cart_item_id"] if "cart_item_id" in body else None
                units = body["units"] if "units" in body else None
                if product_id == None:
                    raise Exception("Product Id is a required field")
                if cart_item_id == None:
                    raise Exception("Cart Item Id is a required field")
                if units == None:
                    raise Exception("Units is a required field")
                
                product = self.product_repo.get(int(product_id))
                if product == None:
                    raise Exception("Product wasn't found")
                
                if product["units"] < units:
                    raise Exception("There aren't much quantity items avaliable")
                
                for item in cart.items:
                    if item.product_id == product_id and item.id == cart_item_id:
                        break
                else: 
                    raise Exception("Product doesn't exists in the cart")
                cart.updated_units(cart_item_id, units)
                new_cart = self.cart_repo.update(cart.get_info(), cart.id)
                self.data = new_cart
                self.message = "Cart Item has been succesfully updated from the cart"
                self.error = True
                self.status = 200
            except Exception as err:
                self.error = True
                self.message = str(err)
                self.status = 500
                self.data = None
            finally:
                self.response = json.dumps({ "data": self.data, "message": self.message, "error": self.error })
                return self.response, self.status, self.headers