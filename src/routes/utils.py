from .. import models
from ..database import SessionLocal, engine


def get_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        print("closing database")
        db.close()
