from flask import Flask

def create_app(config_class=None):
    app = Flask(__name__)

    # Register front-end blueprint
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app