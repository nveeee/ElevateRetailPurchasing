from app import create_app
from app.seed import seed_all

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_all()