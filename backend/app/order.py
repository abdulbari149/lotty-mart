import json
from flask import request
from app.base import BaseService
from app.repository.cart_repository import cart_repo
from app.repository.order_repository import order_repo
from app.repository.product_repository import product_repo
from app.users import UserService
from  models.cart import Cart
from models.order import Order, ShippingInfo
class OrderService(BaseService): 
    def __init__(self, ):
        super().__init__("order")
        self.cart_repo = cart_repo
        self.order_repo = order_repo
        self.product_repo = product_repo
    def register_routes(self):
        @self.app.route("/order/checkout", methods=["POST"])
        def order_checkout():
            try:
                body = request.get_json()
                user_id = body["user_id"] if "user_id" in body else None
                
                shipping_details_body = body["shipping_details"] if "shipping_details" in body else None
                if shipping_details_body == None:
                    raise Exception("Shipping Details aren't provided")
                
                UserService.checkUser(user_id)
                cart = self.cart_repo.get_by_user_id(user_id) 
                if cart == None:
                    raise Exception("Cart doesn't exists for the provided user")
                
                cart_obj = Cart(id=cart["id"], user_id=cart["user_id"], items=cart["items"])
                cart_item_ids: list[int] | None = body["cart_item_ids"] if "cart_item_ids" in body else None
                if cart_item_ids == None:
                    raise Exception("Cart Items Doesn't exists")
                shipping_details_info = ShippingInfo(id=1,**shipping_details_body)
                orders = []
                for item in cart_obj.items.copy():
                    if item.id in cart_item_ids:
                        orders_saved = self.order_repo.get()
                        order_id = 1 if len(orders_saved) == 0 else orders_saved[-1]["id"] + 1
                        order = Order(id=order_id, product_id=item.product_id, user_id=user_id ,shipping_details=shipping_details_info, amount=item.total_amount, units=item.ordered_quantity)
                        if not order.check_order_status():
                            order.status = "delivered"
                        order_info = order.get_info()
                        product = self.product_repo.get(item.product_id)
                        product["units"] -= item.ordered_quantity
                        updated_product = self.product_repo.update(product, product["id"])
                        self.order_repo.add(order_info)
                        orders.append(order_info)
                        cart_obj.remove_cart_item(item.id)
                self.cart_repo.update(cart_obj.get_info(), cart_obj.id)
                self.data = orders
                self.message = "Orders Have Been Executed Successfully"
                self.error = False
                self.status = 200
            except Exception as err:
                self.message = str(err)
                self.error = True
            finally:
                self.response = {"data": self.data, "message": self.message, "error": self.error}
                return self.response, self.status, self.headers
        @self.app.route("/order/get-history")
        def get_orders():
            try:
                user_id = request.args.get("user_id")
                UserService.checkUser(user_id=user_id)
                orders = self.order_repo.get_by_user_id(user_id=user_id)        
                def remove_order(order):
                    order.pop("shipping_details")
                    pid = order.pop("product_id")
                    product = self.product_repo.get(pid)
                    order["product"] = product
                    return order
                mapped_orders = map(remove_order,orders)
                self.data = list(mapped_orders)
                self.message = "Order history List"
                self.error = False
                self.status = 200
            except Exception as err:
                self.error = True
                self.message = str(err)
                self.data = None
                self.status = 500
            finally:
                self.response = {"data": self.data, "message": self.message, "error": self.error}
                return self.response, self.status, self.headers