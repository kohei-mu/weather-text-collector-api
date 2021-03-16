import os
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session

# PostgreSQL用のDBエンジンの作成
connection_uri = os.getenv("POSTGRE_URI")
engine = create_engine(connection_uri, echo=True)
# セッションの作成
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = SessionLocal.query_property()
