from models import db
from .product import Product

class OrderItems(db.Model):
    """Represents an item in an order."""
    order_item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Add this line to establish foreign key relationship
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    
    product = db.relationship('Product', backref='order_items', uselist=False)
    
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))

    def __repr__(self):
        return (f"<OrderItems(order_item_id={self.order_item_id}, "
                f"quantity={self.quantity}, product_id={self.product_id}, "
                f"order_id={self.order_id})>")

