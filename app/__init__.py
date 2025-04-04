from flask import Flask
import logging
from .database import db

def create_app(config_class=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elevate_retail.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Configure logging to terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    stream_handler.setLevel(logging.INFO)
    
    # Add handler to the application logger
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Elevate Retail Purchasing startup')

    # Register front-end blueprint
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register CLI commands
    from .cli import register_commands
    register_commands(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()

    return app
