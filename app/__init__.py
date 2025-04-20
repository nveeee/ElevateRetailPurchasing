import os
import logging
from flask import Flask, redirect
from dotenv import load_dotenv
from .database import db

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
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Elevate Retail Purchasing startup')

    # Register front-end blueprint
    from .main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/purchasing')

    # Register API blueprint
    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/purchasing/api')

    # Register CLI commands
    from .cli import register_commands
    register_commands(app)

    # 👇 Redirect root URL to /purchasing
    @app.route('/')
    def redirect_to_purchasing():
        return redirect('/purchasing/')

    # Standalone Database Mode
    if not os.getenv('FLASK_ENV') or os.getenv('FLASK_ENV') == 'pos':
        with app.app_context():
            db.create_all()

            from sqlalchemy import text
            sql_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db', 'Elevate_Insert.sql'))

            with open(sql_file_path, 'r') as file:
                sql_statements = file.read()

            for statement in sql_statements.strip().split(';'):
                if statement.strip():
                    try:
                        db.session.execute(text(statement))
                    except Exception as e:
                        app.logger.error(f"Failed to execute statement: {statement}\nError: {e}")

            db.session.commit()

    return app
