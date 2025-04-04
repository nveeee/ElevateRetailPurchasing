from flask import Flask
import logging

# TODO: Database connection commented out while working locally
# from .database import engine, Base
# Base.metadata.create_all(bind=engine)

def create_app(config_class=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    
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

    return app