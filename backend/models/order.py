from models.base import BaseModel

class ShippingInfo(BaseModel):
    def __init__(self, id, first_name, last_name, country, state, city, zipCode, contact_no, address_1, address_2, payment_type,credit_card_no, order_notes, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.first_name = first_name
        self.last_name = last_name
        self.country = country
        self.city=city
        self.state = state
        self.zipCode = zipCode
        self.contact_no = contact_no
        self.address_1 = address_1
        self.address_2 = address_2
        self.payment_type = payment_type
        self.credit_card_no = credit_card_no
        self.order_notes = order_notes
        
    def get_info(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "country": self.country,
            "zipCode" : self.zipCode,
            "state": self.state,
            "contact_no" : self.contact_no,
            "address_1": self.address_1,
            "address_2" : self.address_2,
            "payment_type" : self.payment_type,
            "credit_card_no" : self.credit_card_no,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
class Order(BaseModel):
    def __init__(self, id, product_id, user_id ,shipping_details, amount, units ,created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.product_id = product_id
        self.amount = amount
        self.units = units
        self.status = "pending"
        self.user_id = user_id
        if isinstance(shipping_details, ShippingInfo):
            self.shipping_details = shipping_details
    def get_info(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "amount": self.amount,
            "units": self.units,
            "status": self.status,
            "shipping_details": self.shipping_details.get_info(),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    def check_order_status(self):
        if self.status == "pending":
            return False
        elif self.status == "delivered":
            return True