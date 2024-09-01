from models import db

class Product(db.Model):
    """Model representing a product with attributes and relationships."""  
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

    def __repr__(self):
        return (f"<Product(product_id={self.product_id}, product_name='{self.product_name}', "
                f"price=${self.price}, category_id={self.category_id})>")
