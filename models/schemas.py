# Define Marshmallow schemas for serializing the app's SQLAlchemy models.
from models import ma
from models.user import User
from models.product import Product
from models.order import Order
from models.order_items import OrderItems
from models.invoice import Invoice
from models.category import Category
from models.address import Address

class UserSchema(ma.SQLAlchemyAutoSchema):
    # Links the schema to the corresponding SQLAlchemy models.
    class Meta:
        model = User
        
class AddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        
class OrderItemsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItems
        
class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        
class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        
