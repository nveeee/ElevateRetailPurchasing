import os
import logging
from flask import Flask, redirect, session
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
    stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
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

    #  Redirect root URL to login
    @app.route('/')
    def redirect_to_login():
        return redirect('/login')

    #  Login page route
    @app.route('/login')
    def login():
        return '''
        <section style="display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #2c2c2c; color: white; font-family: Arial, sans-serif;">
            <div style="text-align: center; padding: 40px; background: #3a3a3a; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                <img src="/static/images/elevate_retail_logo.jpg" alt="Logo" style="width: 200px; margin-bottom: 20px;" />
                <h2>Welcome to Elevate Retail</h2>
                <p>Please log in to continue</p>
                <a href="/purchasing" 
                   style="display: inline-block; margin-top: 20px; padding: 12px 24px; background-color: #B5C8B8; color: white; font-size: 1.2rem; border-radius: 6px; text-decoration: none; transition: background-color 0.3s ease;"
                   onmouseover="this.style.backgroundColor='#28a745';"
                   onmouseout="this.style.backgroundColor='#B5C8B8';">
                   Log In
                </a>
            </div>
        </section>
        '''

    #  Logout route to clear session and redirect to login
    @app.route('/logout')
    def logout():
        session.clear()  # Clears the session to log out the user
        return redirect('/login')  # Redirect to the login page

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
