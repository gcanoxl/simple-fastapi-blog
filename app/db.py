from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .configs import config

dbconfig = config.configs.db
DATABASE_URL = f"mysql+pymysql://{dbconfig['user']}:{dbconfig['password']}@{dbconfig['host']}:{dbconfig['port']}/{dbconfig['database']}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
