from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import DATABASE_URL, MONGODB_URL
from app.models.user import User as MongoUser

Base = declarative_base()

# PostgreSQL setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MongoDB setup
client = AsyncIOMotorClient(MONGODB_URL)
database = client.get_default_database()

async def init_db():
    await init_beanie(database, document_models=[MongoUser])