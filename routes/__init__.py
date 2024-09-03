from .user_routes import user_routes
from .product_routes import product_routes
from .cart_routes import cart_routes

def register_routes(app):
    app.register_blueprint(user_routes)
    app.register_blueprint(product_routes)
    app.register_blueprint(cart_routes)

