from models import db
from datetime import datetime

class Invoice(db.Model):
    """Represents an invoice for an user-order."""
    invoice_id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=False)
    invoice_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    
    def __repr__(self):
        return (f"<Invoice(invoice_id={self.invoice_id}, total_amount={self.total_amount}, "
                f"invoice_date={self.invoice_date}, payment_method='{self.payment_method}', "
                f"user_id={self.user_id}, order_id={self.order_id})>")
