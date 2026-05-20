from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from setting import settings
print(settings.DB_CONNECTION)


Base = declarative_base()

engine = create_engine(url = settings.DB_CONNECTION)

session_Local = sessionmaker(bind=engine)


def get_db():
    db = session_Local()
    try:
        yield db
    finally:
        db.close()    