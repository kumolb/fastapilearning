from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

connection_url = "postgresql://postgres:kumol254@localhost/fastapi"

engine = create_engine(connection_url)

sessionLocal = sessionmaker(autoflush=False, autocommit = False, bind= engine )
Base = declarative_base()