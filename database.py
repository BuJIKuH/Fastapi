from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:9830@localhost:5432/template1"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session = sessionmaker(bind=engine)

Base = declarative_base()
