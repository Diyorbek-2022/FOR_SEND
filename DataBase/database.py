from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///Unknown_Science.db', echo=True)
"""
POSTGRES DATABASE
'postgresql://postgres:1234@localhost/delivery_db'

SQLITE DATABASE
'sqlite:///Unknown_Science.db'
"""


Base = declarative_base()
session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
