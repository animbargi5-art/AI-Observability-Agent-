from sqlalchemy import create_engine

from app.database.models import Base


DATABASE_URL = "sqlite:///./tattvaai.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


def create_tables():

    Base.metadata.create_all(bind=engine)