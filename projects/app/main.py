from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import pygeohash
import pickle
import logging
from . import models, schemas
from .sql import (
  get_algorithm_by_tag,
  get_model_by_tag
)
from .database import (
  SessionLocal, 
  engine
)
from .ml import (
  hukai_calc,
  kanso_calc,
  ne2string,
  sent2score,
  hotelling
)

# テーブル作成
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# セッションを生成
def get_db():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()

# TEST
@app.get('/hello')
async def hello():
  return 'Welcome! MyApp!'

# ジオハッシュ取得用API
@app.post('/geohash', response_model=schemas.GeohashOut, response_model_exclude_unset=True)
async def geohash(data: schemas.GeohashIn):
  geo_encode = pygeohash.encode(data.lat, data.lon)
  return {'geohash': geo_encode}

# 不快係数API
@app.post('/hukai', response_model=schemas.HukaiOut, response_model_exclude_unset=True)
async def hukai(data: schemas.HukaiIn):
  hukai = hukai_calc(data.temp, data.humid)
  return {'hukai': hukai}

# 乾燥係数API
@app.post('/kanso', response_model=schemas.KansoOut, response_model_exclude_unset=True)
async def kanso(data: schemas.KansoIn):
  kanso = kanso_calc(data.humid)
  return {'kanso': kanso}

# 固有表現抽出API
@app.post('/neget', response_model=schemas.NEGetOut, response_model_exclude_unset=True)
async def neget(data: schemas.NEGetIn):
  ne_string = ne2string(data.text, data.lang)
  return {'nestring': ne_string}

# SentimentAnalysisAPI
@app.post('/sentget', response_model=schemas.SentGetOut, response_model_exclude_unset=True)
async def sentget(data: schemas.SentGetIn):
  sent_score = sent2score(data.text, data.lang)
  return {'sentscore': sent_score}

# 異常検知用API
@app.post("/anomaly", response_model=schemas.AnomalyOut, response_model_exclude_unset=True)
async def anomaly(data: schemas.AnomalyIn, db: Session = Depends(get_db)):
  # タグに該当するアルゴリズムの取得
  algorithm = get_algorithm_by_tag(db=db, tag=data.tag)
  # アルゴリズムが見つからなかった場合
  if algorithm == None:
    message = f"Algorithm Not Found for tag:{data.tag}"
    logging.error(message)
    raise HTTPException(status_code=500, detail=message)
  else:
    algorithm = algorithm[0]

  # タグ及びアルゴリズムに該当するモデルファイルの取得
  model = get_model_by_tag(db=db, tag=data.tag, algorithm=algorithm)
  # モデルファイルが見つからなかった場合
  if model == None:
    message = f"Modelfile Not Found for tag:{data.tag} and algorithm:{algorithm}"
    logging.error(message)
    raise HTTPException(status_code=500, detail=message)
  else:
    model = pickle.loads(model[0])

  # 異常検知モデルの適用
  # 取得したアルゴリズムの推論用コードが未実装の場合
  if algorithm not in globals():
    message = f"Algorithm:{algorithm} Not Implemented"
    logging.error(message)
    raise HTTPException(status_code=500, detail=message)
  else:
    try:
      anomaly_score, threshold, anomalyresult = globals()[algorithm](data.value, model)
    # モデルの適用に失敗した場合
    except:
      message = f"Algorithm:{algorithm} Inference Failed"
      logging.error(message)
      raise HTTPException(status_code=500, detail=message)

  ret_obj = {
    'algorithm':algorithm,
    'anomalyscore':anomaly_score,
    'threshold':threshold,
    'anomalyresult':anomalyresult
  }
  return ret_obj
