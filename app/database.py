from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace these with your actual database credentials
SQLSERVER_HOST = "your_server"
SQLSERVER_DATABASE = "your_database"
SQLSERVER_USER = "your_username"
SQLSERVER_PASSWORD = "your_password"

# Create the connection URL
DATABASE_URL = f"mssql+pymssql://{SQLSERVER_USER}:{SQLSERVER_PASSWORD}@{SQLSERVER_HOST}/{SQLSERVER_DATABASE}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
