from flask import Flask, jsonify, request
from models import db, ma
from werkzeug.security import generate_password_hash
from models.user import User
from models.product import Product
from models.category import Category
from models.order import Order
from models.order_items import OrderItems
from models.invoice import Invoice
from models.address import Address
from models.schemas import UserSchema, CategorySchema, ProductSchema, OrderSchema, OrderItemsSchema, InvoiceSchema, AddressSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db.init_app(app)
ma.init_app(app)

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
    
#     if not data or not data.get('user_name') or not data.get('email') or not data.get('password'):
#         return jsonify({"message": "User name, email, and password are required."}), 400
    
#     if User.query.filter_by(email=data['email']).first():
#         return jsonify({"message": "Email already exists."}), 409
    
#     hashed_password = generate_password_hash(data['password'], method='sha256')
    
#     new_user = User(
#         user_name=data['user_name'],
#         email=data['email'],
#         role=data.get('role', 'customer'),
#         password_hash=hashed_password
#     )
    
#     db.session.add(new_user)
#     db.session.commit()
    
#     return jsonify({"message": "User registered successfully."}), 201

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    with app.app_context():
        create_tables()  
    app.run(debug=True)
