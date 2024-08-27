from models import db

class Category(db.Model):
    """ Represents a product category."""
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(200), nullable=False)

    product = db.relationship('Product',backref="product")

    def __repr__(self):
        return (f"<Category(category_id={self.category_id}, "
                f"category_name='{self.category_name}')>")