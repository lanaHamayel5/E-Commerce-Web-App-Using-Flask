from flask import Flask
from models import db, ma, migrate
from routes import register_routes
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager
from models.user import User  
from datetime import timedelta
import os

app = Flask(__name__)

# Configure the DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', b'|f\xa3\xf5\xc7=x\xa0\xca\xad[i\xaf\xde\x07\xfe\xfez"\xba\xcc\xec@\xf7\x1f\x19"|!\x9ah\x8f')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

db.init_app(app)
ma.init_app(app)
migrate.init_app(app, db)

register_routes(app)

def seed_data():
    """This function seeds initial data into the database."""
    admin_hashed_password = generate_password_hash("Omar123#", method='pbkdf2:sha256')
    user_hashed_password = generate_password_hash("Ali321@", method='pbkdf2:sha256')

    with app.app_context():
        if not User.query.filter_by(email="Omar12.amjad@gmail.com").first():
            admin = User(user_name="Omar Amjad", email="Omar12.amjad@gmail.com", role='admin', password_hash=admin_hashed_password)
            db.session.add(admin)

        if not User.query.filter_by(email="Ali.kareem@gmail.com").first():
            user1 = User(user_name="Ali Kareem", email="Ali.kareem@gmail.com", role='customer', password_hash=user_hashed_password)
            db.session.add(user1)
        
        db.session.commit()

def create_tables():
    """This function creates all the database tables."""
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    with app.app_context():
        create_tables()
        seed_data()
    app.run(debug=True)
