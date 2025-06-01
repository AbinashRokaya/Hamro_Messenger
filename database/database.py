from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
DATABASE_URL="postgresql://postgres:abinash@localhost:5432/messanger" 

engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base=declarative_base()


@contextmanager
def get_db() -> Session:
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()