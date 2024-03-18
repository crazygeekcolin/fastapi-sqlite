from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Windows alternative using raw string
#engine = create_engine(r'sqlite:///C:\path\to\foo.db')

SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()