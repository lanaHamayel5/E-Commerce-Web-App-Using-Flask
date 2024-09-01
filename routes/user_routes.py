from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.user import User
from models.schemas import UserSchema
from models import db
import re

# Create a Blueprint for user-related routes
user_routes = Blueprint('user_routes', __name__)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_strong_password(password):
    return len(password) >= 8

@user_routes.route('/register', methods=['POST'])
def register():
    """ Registers a new user."""
    data = request.json

    if not data or not data.get('user_name') or not data.get('email') or not data.get('password'):
        return jsonify({"message": "User name, email, and password are required."}), 400

    if not is_valid_email(data['email']):
        return jsonify({"message": "Invalid email format."}), 400

    if not is_strong_password(data['password']):
        return jsonify({"message": "Password must be at least 8 characters long."}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists."}), 409

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    new_user = User(
        user_name=data['user_name'],
        email=data['email'],
        role=data.get('role', 'customer'),
        password_hash=hashed_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while registering the user.", "error": str(e)}), 500

    return jsonify({"message": "User registered successfully."}), 201


@user_routes.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user by checking email and password.
    """
    data = request.json
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': "Email and password are required."}), 400

    if not is_valid_email(data['email']):
        return jsonify({"message": "Invalid email format."}), 400

    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"message": "Invalid email or password."}), 401
    
    # Generate a JWT token
    access_token = create_access_token(identity=user.user_id)
    
    return jsonify({"message": "Login successful.", "token": access_token}), 200


@user_routes.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Fetch user profile details."""
    current_user_id = get_jwt_identity()
    
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404
    
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user)), 200
