from sqlmodel import Session, create_engine
from models import SQLModel
from config import settings

DATABASE_URL = settings.DATABASE_URL

# DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(bind=engine,autocommit=False,autoflush=False) as db:
        yield db