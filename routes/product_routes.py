from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.product import Product
from models.user import User
from models.schemas import ProductSchema
from models import db


# Create a Blueprint for product-related routes
product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/products',methods=['POST'])
@jwt_required()
def create_product():
    
    data = request.json
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin':
        return jsonify({"message" : "You are not authorized to perform this action."}),403
    
    new_product = Product(
        product_name = data['name'],
        price = data['price'],
        description = data['description'],
        product_quantity = data['quantity']
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({"message" : "Product created successfully.","product_id":new_product.product_id}), 201
    