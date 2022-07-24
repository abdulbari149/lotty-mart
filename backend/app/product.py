import json
from unittest import result
from xml.dom import ValidationErr
from flask import Blueprint, Response, jsonify, redirect, request
from app.base import BaseService
from errors.notFound import NotFoundError
from models.product import  Product
from app.repository.product_repository import product_repo
from app.repository.cart_repository import cart_repo

class ProductService(BaseService):
    def __init__(self):
        super().__init__(name="product")
        self.product_repo = product_repo
    def register_routes(self):
        @self.app.route("/product/get", methods=["GET"])
        def get_all_products():
            try:
                products = self.product_repo.get()
                if not products:
                    raise NotFoundError("Product's doesn't exists")
                self.data = products
                self.error = None
                self.message = "Products List"
                self.status = 200
            except NotFoundError as err: 
                self.error = True
                self.message = str(err)
                self.data = None
                self.status = 404
            finally:
                self.response = json.dumps({ "data": self.data, "message": self.message, "error": self.error })
                return self.response, self.status, self.headers
        @self.app.route("/product/get/<int:product_id>")
        def get_product_by_id(product_id):
            try:
                product = self.product_repo.get(int(product_id))
                print(product)
                if not product:
                    raise NotFoundError("Product wasn't Not Found")
                self.data = product
                self.error = False
                self.message = f"Product with id {product_id}"
                self.status = 200                
            except NotFoundError as err: 
                self.error = True
                self.message = str(err)
                self.data = None
                self.status = 404
            finally:
                self.response = json.dumps({ "data": self.data, "message": self.message, "error": self.error })
                return self.response, self.status, self.headers
        @self.app.route("/product/add", methods=["POST"])
        def add_product():
            try:
                data = dict(request.get_json())
                products = self.product_repo.get()
                new_id = products[-1]["id"] + 1 
                if "name" not in data or data["name"] == "" or data["name"] == None:
                    raise Exception("name is required")
                if "description" not in data or data["description"] == "" or data["description"] == None:
                    raise Exception("description is required")
                if "price" not in data or data["price"] == None:
                    raise Exception("price is required")
                if type(data["price"]) != int:
                    raise Exception("Price should be an integer value")
                if "brand_name" not in data or data["brand_name"] == "" or data["brand_name"] == None:
                    raise Exception("brand_name is required")
                if "category" not in data or data["category"] == "" or data["category"] == None:
                    raise Exception("category is required")
                if data["category"] not in ("food", "electronic_devices", "clothes"):
                    raise Exception("Category is invalid")
                if "warranty" not in data or data["warranty"] == "" or data["warranty"] == None:
                    raise Exception("warranty is required")
                if "units" not in data or data["units"] == "" or data["units"] == None:
                    raise Exception("units is required")
                if type(data["units"]) != int:
                    raise Exception("Units can only be of type integer")
                if data["units"] < 0:
                    raise Exception("Units cannot be a negative value")
                if "packaging_type" not in data or data["packaging_type"] == "" or data["packaging_type"] == None:
                    raise Exception("packaging_type is required")
                if "details" not in data or data["details"] == None:
                    raise Exception("details is required")
                if "image_name" not in data or data["image_name"] == None or data["image_name"] == "":
                    raise Exception("Image Name is required")
                name = data["name"]
                description = data["description"]
                price = data["price"]
                make = data["make"]
                category = data["category"]
                brand_name = data["brand_name"]
                warranty=data["warranty"]
                image_name = data["image_name"]
                packaging_type = data["packaging_type"]
                shipping_fare = data["shipping_fare"]
                units = int(data["units"]) 
                details = data["details"]
                product = Product(new_id, name=name,price=price, description=description ,make=make,image_name=image_name,category=category, brand_name=brand_name,warranty=warranty, packaging_type=packaging_type, shipping_fare=shipping_fare, units=units, details=details)
                result = self.product_repo.add(product.get_info())
                if result != True:
                    raise Exception(result)
                self.data = product.get_info()
                self.message = "Product was added successfully"
                self.status = 201
                self.error = False
            except TypeError as err:
                self.error = True
                self.data = None
                self.status = 403
                self.message = str(err)
                self.status = 500
            except Exception as err:
                self.error = True
                self.data = None
                self.message = str(err)
                self.status = 500
            finally:
                self.response = json.dumps({ "data": self.data, "message": self.message, "error": self.error })    
                return self.response, self.status, self.headers 
        
# class ProductService(BaseService):
#     def __init__(self):
#     		super().__init__(ProductRepository)
# class ProductController(Product):      
#         @product.route("")
#         def get_all_products():
#             with open("data/product.json") as product_file:
#                 data =json.load(product_file)
#                 return json.dumps(data)
#         @product.route("/product/get-product/<product_id>")
#         def get_product(product_id):
#               with open('data/product.json') as proudct_file:
#                 data =json.load(proudct_file)
#                 p_id =int(product_id)
#                 if len(data) <= p_id:
#                       return "Product not found"
#                 return data[p_id]
              
              
#         @product.route("/product/add-product", methods=["POST"])
#         def add_product():
#           name = request.form.get("name")
#           price = int(request.form.get("price"))
#           category = request.form.get("category").upper()
#           category = CategoryEnum[category]
#           created_at = datetime.datetime.now()
#           updated_at = datetime.datetime.now()
          
#           print("Name: " + name,"Price: "+price)
#           with open("data/product.json") as product_file:
#             products = json.load(product_file)
#             products.append()
#             data = products
          
#           with open("data/product.json", "w") as w_product_file:
#             product_json = json.dumps(data)	
#             w_product_file.write(product_json)
            
#           return redirect("/display-product")