from .user_routes import user_routes
from .product_routes import product_routes

def register_routes(app):
    app.register_blueprint(user_routes)
    app.register_blueprint(product_routes)
