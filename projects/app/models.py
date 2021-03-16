from sqlalchemy import Column, String, Float, DateTime, LargeBinary
from .database import Base
import os

anomaly_model = os.getenv("ANOMALY_TABLE_MODEL")
anomaly_algorithm = os.getenv("ANOMALY_TABLE_ALGORITHM")

# モデルテーブル用のテーブル定義
class Model(Base):
  _schema = anomaly_model.split('.')[0]
  _table = anomaly_model.split('.')[1]
  __table_args__ = {'schema': _schema,'extend_existing': True}
  __tablename__ = _table
  timestamp = Column(DateTime, primary_key=True)
  tag = Column(String)
  algorithm = Column(String)
  modelfile = Column(LargeBinary)
  modelparameters = Column(String)

# アルゴリズムテーブル用のテーブル定義
class Algorithm(Base):
  _schema = anomaly_algorithm.split('.')[0]
  _table = anomaly_algorithm.split('.')[1]
  __table_args__ = {'schema': _schema,'extend_existing': True}
  __tablename__ = _table
  tag = Column(String, primary_key=True)
  algorithm = Column(String)
