from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.product import Product
from models.order import Order
from models.order_items import OrderItems
from models.invoice import Invoice
from models import db

# Create a Blueprint for cart-related routes
cart_routes = Blueprint('cart_routes', __name__)


@cart_routes.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """
    Retrieve the current user's cart details, including order items and invoice.

    Returns:
        JSON response with order details including:
        - order_id: ID of the current order
        - total_amount: Total amount for the order
        - products: List of products in the cart with details (ID, name, quantity, price)
        - date: Formatted invoice date
    
    HTTP Status Codes:
        - 200 OK: If the order and invoice are successfully retrieved
        - 404 Not Found: If no active order or invoice is found for the user
    """
    current_user = get_jwt_identity()

    # Fetch the order and its items
    order = Order.query.filter_by(user_id=current_user).first()
    if not order:
        return jsonify({'message': 'No active order found for user'}), 404

    invoice = Invoice.query.filter_by(order_id=order.order_id).first()
    if not invoice:
        return jsonify({'message': 'No invoice found for the order'}), 404
 
    # Fetch order items and product details
    order_items = OrderItems.query.filter_by(order_id=order.order_id).all()
    products = []
    for item in order_items:
        product = Product.query.get(item.product_id)
        if product:
            products.append({
                'product_id': product.product_id,
                'name': product.product_name,
                'quantity': item.quantity,
                'price': str(product.price)
            })

   
    formatted_date = invoice.invoice_date.strftime('%Y-%m-%d %H:%M:%S')

    # Return order and invoice details
    return jsonify({
        'order_id': order.order_id,
        'total_amount': invoice.total_amount,
        'products': products,
        'date': formatted_date
    })
    
    
@cart_routes.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    """
    Add products to the current user's cart or create a new order if none exists.
    
    Returns:
        JSON response with a success message and order ID.
    
    HTTP Status Codes:
        - 200 OK: If products are successfully added to the cart
        - 400 Bad Request: If input data is invalid or stock is insufficient
        - 404 Not Found: If any of the products are not found
        - 500 Internal Server Error: If an error occurs during database operations
    """
    current_user = get_jwt_identity()
    data = request.json
    
    # Extract products and order details from request data
    products = data.get('products', [])
    way_of_buying = data.get('way_of_buying', 'Online Payment')  # Default value
    
    # status= data.get('status', 'Pending')
    
    for product_info in products:
        quantity = product_info.get('quantity')
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({'error': 'Invalid quantity provided'}), 400


    # Check if an order already exists for the user, otherwise create a new one
    order = Order.query.filter_by(user_id=current_user, status='Pending').first()
    if not order:
        order = Order(user_id=current_user, status='Pending')
        db.session.add(order)
        db.session.commit()
    
    total_amount = 0
    
    for product_info in products:
        product_name = product_info['name']
        quantity = product_info['quantity']
        
        product = Product.query.filter_by(product_name=product_name).first()
        
        if not product:
            return jsonify({'error': f'Product {product_name} not found'}), 404
        
        if product.product_quantity < quantity:
            return jsonify({'message': f'Insufficient stock for product {product_name}'}), 400
        
        order_item = OrderItems(quantity=quantity, product_id=product.product_id, order_id=order.order_id)
        db.session.add(order_item)
        
        product.product_quantity -= quantity
        
        total_amount += product.price * quantity

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    invoice = Invoice.query.filter_by(order_id=order.order_id).first()
    
    if not invoice:
        invoice = Invoice(
            total_amount=total_amount,
            payment_method=way_of_buying,
            order_id=order.order_id,
            user_id=current_user
        )
        db.session.add(invoice)
    else:
        invoice.total_amount = total_amount
        invoice.payment_method = way_of_buying

    try:
        db.session.commit()
        return jsonify({'message': 'Products added to cart successfully', 'order_id': order.order_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    
@cart_routes.route('/cart', methods=['PUT'])
@jwt_required()
def update_cart():
    """
    Update the quantities of products in the current user's cart.
    
    Returns:
        JSON response with a success message and order ID.
    
    HTTP Status Codes:
        - 200 OK: If the cart is successfully updated
        - 400 Bad Request: If input data is invalid or stock is insufficient
        - 404 Not Found: If any of the products are not found or not in the cart
        - 500 Internal Server Error: If an error occurs during database operations
    """
    current_user = get_jwt_identity()
    data = request.json

    products = data.get('products', [])
    if not products:
        return jsonify({'error': 'No products provided'}), 400
    
    order = Order.query.filter_by(user_id=current_user, status='Pending').first()
    if not order:
        return jsonify({'error': 'No pending order found for user'}), 404

    total_amount = 0

    for product_info in products:
        product_name = product_info['name']
        new_quantity = product_info['quantity']
        
        product = Product.query.filter_by(product_name=product_name).first()
        if not product:
            return jsonify({'error': f'Product {product_name} not found'}), 404
        

        order_item = OrderItems.query.filter_by(order_id=order.order_id, product_id=product.product_id).first()
        if not order_item:
            return jsonify({'error': f'Product {product_name} is not in the cart'}), 404
        
    
        stock_change = new_quantity - order_item.quantity
        
        if product.product_quantity < stock_change:
            return jsonify({'message': f'Insufficient stock for product {product_name}'}), 400
        
        
        order_item.quantity = new_quantity
        
        product.product_quantity -= stock_change

        total_amount += product.price * new_quantity

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    invoice = Invoice.query.filter_by(order_id=order.order_id).first()
    if invoice:
        invoice.total_amount = total_amount
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Cart updated successfully', 'order_id': order.order_id}), 200


@cart_routes.route('/cart/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """
    Clear all items from the current user's cart.
    
    Returns:
        JSON response with a success message.
    
    HTTP Status Codes:
        - 200 OK: If the cart is successfully cleared
        - 404 Not Found: If no pending order is found for the user
        - 500 Internal Server Error: If an error occurs during database operations
    """
    current_user = get_jwt_identity()

    order = Order.query.filter_by(user_id=current_user, status='Pending').first()
    if not order:
        return jsonify({'error': 'No pending order found for user'}), 404

    order_items = OrderItems.query.filter_by(order_id=order.order_id).all()
    total_amount = 0

    for item in order_items:
        product = Product.query.get(item.product_id)
        if not product:
            continue
        
        product.product_quantity += item.quantity
        
        total_amount += product.price * item.quantity

        db.session.delete(item)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    invoice = Invoice.query.filter_by(order_id=order.order_id).first()
    if invoice:
        db.session.delete(invoice)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    db.session.delete(order)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Cart cleared successfully'}), 200
