from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.product import Product
from models.user import User
from models.schemas import ProductSchema
from models import db


# Create a Blueprint for product-related routes
product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/products',methods=['GET'])
@jwt_required()
def get_all_products():
    """Get all products."""
     
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'admin':
        return jsonify ({"message": "You are not authorized to perform this action."}),403
    
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    return jsonify(product_schema.dump(products)), 200


@product_routes.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product_by_id(product_id):
    """Get a product by its ID."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'admin':
        return jsonify({"message": "You are not authorized to perform this action."}), 403
    
    # Retrieve the product by its ID
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({"message": "Product not found."}), 404
    
    # Serialize the single product object
    product_schema = ProductSchema()
    return jsonify(product_schema.dump(product)), 200


@product_routes.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    """Add a new product."""
    data = request.json
    
    if not data.get('name') or not isinstance(data.get('name'), str):
        return jsonify({"message": "Product name must be a non-empty string."}), 400
    
    if not data.get('price') or not isinstance(data.get('price'), (int, float)) or data.get('price') < 0:
        return jsonify({"message": "Invalid price"}), 400
    
    if not data.get('quantity') or not isinstance(data.get('quantity'), int) or data.get('quantity') < 0:
        return jsonify({"message": "Invalid quantity"}), 400
    
    if not data.get('category_id') or not isinstance(data.get('category_id'), int) or data.get('category_id') < 0:
        return jsonify({"message": "Invalid category ID"}), 400
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if current_user.role != 'admin':
        return jsonify({"message": "You are not authorized to perform this action."}), 403
    
    new_product = Product(
        product_name=data['name'],
        price=data['price'],
        description=data['description'],
        product_quantity=data['quantity'],
        category_id=data['category_id']  # Include category_id
    )
    
    try:
        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while adding the product.", "error": str(e)}), 500
    
    return jsonify({"message": "Product created successfully.", "product_id": new_product.product_id}), 201

    
@product_routes.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Update an existing product by its ID."""
    data = request.json
    
    # Input Validation
    if 'name' in data and (not isinstance(data['name'], str)):
        return jsonify({"message": "Invalid product name."}), 400
    
    if 'price' in data and (not isinstance(data['price'], (int, float)) or data['price'] < 0):
        return jsonify({"message": "Invalid price."}), 400
    
    if 'quantity' in data and (not isinstance(data['quantity'], int) or data['quantity'] < 0):
        return jsonify({"message": "Invalid quantity."}), 400
    
    if 'category_id' in data and (not isinstance(data['category_id'], int) or data['category_id'] < 0):
        return jsonify({"message": "Invalid category ID."}), 400
    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if user.role != 'admin':
        return jsonify({"message": "Access forbidden: Admins Only."}), 403
    
    updated_product = Product.query.filter_by(product_id=product_id).first()
    
    if not updated_product:
        return jsonify({"message": "Product not found."}), 404
    
    # Update the product's attributes
    if 'name' in data:
        updated_product.product_name = data['name']
        
    if 'description' in data:
        updated_product.description = data['description']
        
    if 'price' in data:
        updated_product.price = data['price']
        
    if 'quantity' in data:
        updated_product.product_quantity = data['quantity']
    
    if 'category_id' in data:
        updated_product.category_id = data['category_id']
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while updating the product.", "error": str(e)}), 500
    
    product_schema = ProductSchema()
    return jsonify(product_schema.dump(updated_product)), 200


@product_routes.route('/products/<int:product_id>',methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Delete a product by its ID."""

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    
    if user.role != 'admin':
        return jsonify({"message": "Access forbidden: Admins Only."}), 403
    
    delete_product = Product.query.get(product_id)
    
    if not delete_product:
        return jsonify({"message": "Product not found."}), 404

    try:
        db.session.delete(delete_product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the product.", "error": str(e)}), 500
    
    return jsonify({"message": "Product successfully deleted."}), 200