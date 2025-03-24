# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

  
# Replace with your PostgreSQL credentials
SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_WwV3RkKMSo1v@ep-dark-wave-a55eyxsj-pooler.us-east-2.aws.neon.tech/niver_princesa"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)
