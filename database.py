from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///users.db', echo = True)
db_session = scoped_session(sessionmaker(bind=engine))()

Base = declarative_base()
# Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)




