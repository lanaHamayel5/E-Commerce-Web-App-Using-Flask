from models import db
from datetime import datetime

class User(db.Model):
    """Model representing a user with attributes and relationships."""    
    user_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_name = db.Column(db.String(120), nullable=False,index=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    address = db.relationship('Address',backref='user',uselist=False)
    invoice = db.relationship('Invoice',backref='user')
    order = db.relationship('Order',backref='user')
   
    
    def __repr__(self):
        address_repr = repr(self.address) if self.address else 'None'
        return (f"<User(id={self.id}, user_name='{self.user_name}', email='{self.email}', "
                f"role='{self.role}', password_hash='******', created_at='{self.created_at}', "
                f"address={address_repr})>")