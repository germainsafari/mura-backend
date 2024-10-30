# backend/app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

# Initialize extensions without associating them with the app yet
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    
    # Load configuration from config file
    app.config.from_object(Config)
    
    # Initialize extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register Blueprints (for authentication and chat routes)
    from routes import auth_blueprint, chat_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
    app.register_blueprint(chat_blueprint, url_prefix="/api/chat")

    # Create tables if they don't already exist
    with app.app_context():
        db.create_all()

    return app

# Main entry point
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
