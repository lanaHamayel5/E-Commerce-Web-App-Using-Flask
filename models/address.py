from models import db

class Address(db.Model):
    """ Represents an address for a user."""
    address_id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

       
    def __repr__(self):
        return (f"<Address(address_id={self.address_id}, street='{self.street}', city='{self.city}', "
                f"state='{self.state}', postal_code='{self.postal_code}', country='{self.country}')>")