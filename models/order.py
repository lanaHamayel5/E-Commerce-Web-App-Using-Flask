from models import db
from datetime import datetime

class Order(db.Model):
    """Model representing an order with attributes and relationships."""  
    order_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    order_item = db.relationship('OrderItems',backref='order')
    invoice = db.relationship('Invoice',backref='order',uselist=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'))
    def __repr__(self):
        return (f"<Order(order_id={self.order_id}, status='{self.status}', "
                f"order_date='{self.order_date}', user_id={self.user_id})>")