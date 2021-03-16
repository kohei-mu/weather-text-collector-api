from sqlalchemy.orm import Session
from . import models
from sqlalchemy import and_, desc

# タグを元にアルゴリズムを取得する
def get_algorithm_by_tag(db: Session, tag: str):
  return db.query( models.Algorithm.algorithm )\
      .filter( models.Algorithm.tag == tag )\
      .first()

# タグを元に最新のモデル（バイナリファイル）を取得する
def get_model_by_tag(db: Session, tag: str, algorithm: str):
  return db.query( models.Model.modelfile )\
      .filter( and_( models.Model.tag == tag, models.Model.algorithm == algorithm ) )\
      .order_by( desc( models.Model.timestamp ) )\
      .first()