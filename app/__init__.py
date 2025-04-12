import os
from flask import Flask
import logging
from .database import db
from dotenv import load_dotenv

load_dotenv()


def create_app(config_class=None):
    if not os.getenv('SECRET_KEY') or not os.getenv('SQLALCHEMY_DATABASE_URI'):
        raise EnvironmentError(
            "Missing environment variable(s): SECRET_KEY or SQLALCHEMY_DATABASE_URI"
        )

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
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
    app.register_blueprint(main_bp, url_prefix='/purchasing')

    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/purchasing/api')

    # Register CLI commands
    from .cli import register_commands
    register_commands(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
