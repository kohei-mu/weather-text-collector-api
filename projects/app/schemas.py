from pydantic import BaseModel, validator
import numpy as np

# ジオハッシュ取得用API
class GeohashIn(BaseModel):
  lon: float
  lat: float
  @validator('lon')
  def lon_validate(cls, v):
    if type(v) is not float:
      raise ValueError(f'{v} must be float')
    return v
  @validator('lat')
  def lat_validate(cls, v):
    if type(v) is not float:
      raise ValueError(f'{v} must be float')
    return v
class GeohashOut(BaseModel):
  geohash: str
  @validator('geohash')
  def geohash_validate(cls, v):
    if type(v) is not str:
      raise ValueError(f'{v} must be str')
    elif len(v) < 1:
      raise ValueError(f'{v} must be longer than 0')
    else:
      pass
    return v

# 不快係数API
class HukaiIn(BaseModel):
  temp: float
  humid: float
  @validator('temp')
  def temp_validate(cls, v):
    if type(v) is not float:
      raise ValueError(f'{v} must be float')
    return v
  @validator('humid')
  def humid_validate(cls, v):
    if type(v) is not float:
      raise ValueError(f'{v} must be float')
    return v
class HukaiOut(BaseModel):
  hukai: float
  @validator('hukai')
  def hukai_validate(cls, v):
    if type(v) is not float:
      raise ValueError(f'{v} must be float')
    return v

# 乾燥係数API
class KansoIn(BaseModel):
  humid: float
  @validator('humid')
  def humid_validate(cls, v):
    if type(v) is not float:
      raise ValueError(f'{v} must be float')
    return v
class KansoOut(BaseModel):
  kanso: float
  @validator('kanso')
  def kanso_validate(cls, v):
    if type(v) is not float:
      raise ValueError(f'{v} must be float')
    return v

# 固有表現抽出API
class NEGetIn(BaseModel):
  text: str
  lang: str
  @validator('text')
  def text_validate(cls, v):
    if type(v) is not str:
      raise ValueError(f'{v} must be str')
    elif len(v) < 1:
      raise ValueError(f'{v} must be longer than 0')
    else:
      pass
    return v
  @validator('lang')
  def lang_validate(cls, v):
    if type(v) is not str:
      raise ValueError(f'{v} must be str')
    elif len(v) < 1:
      raise ValueError(f'{v} must be longer than 0')
    else:
      pass
    return v
class NEGetOut(BaseModel):
  nestring: str
  @validator('nestring')
  def nestring_validate(cls, v):
    if type(v) is not str:
      raise ValueError(f'{v} must be str')
    return v

# SentimentAnalysisAPI
class SentGetIn(BaseModel):
  text: str
  lang: str
  @validator('text')
  def text_validate(cls, v):
    if type(v) is not str:
      raise ValueError(f'{v} must be str')
    elif len(v) < 1:
      raise ValueError(f'{v} must be longer than 0')
    else:
      pass
    return v
  @validator('lang')
  def lang_validate(cls, v):
    if type(v) is not str:
      raise ValueError(f'{v} must be str')
    elif len(v) < 1:
      raise ValueError(f'{v} must be longer than 0')
    else:
      pass
    return v
class SentGetOut(BaseModel):
  sentscore: float
  @validator('sentscore')
  def sentscore_validate(cls, v):
    if type(v) is not float:
      raise ValueError(f'{v} must be float')
    return v

# 異常検知用API
class AnomalyIn(BaseModel):
  value: float
  tag: str
  @validator('value')
  def value_validate(cls, v):
    if type(v) not in (float, np.float64):
      raise ValueError(f'{v} must be float')
    return v
  @validator('tag')
  def tag_validate(cls, v):
    if type(v) is not str:
      raise ValueError(f'{v} must be str')
    elif len(v) < 1:
      raise ValueError(f'{v} must be longer than 0')
    else:
      pass
    return v
class AnomalyOut(BaseModel):
  algorithm: str
  anomalyscore: float
  threshold: float
  anomalyresult: int
  @validator('algorithm')
  def algorithm_validate(cls, v):
    if type(v) is not str:
      raise ValueError(f'{v} must be str')
    elif len(v) < 1:
      raise ValueError(f'{v} must be longer than 0')
    else:
      pass
    return v
  @validator('anomalyscore')
  def anomalyscore_validate(cls, v):
    if type(v) not in (float, np.float64):
      raise ValueError(f'{v} must be float')
    return v
  @validator('threshold')
  def threshold_validate(cls, v):
    if type(v) not in (float, np.float64):
      raise ValueError(f'{v} must be float')
    return v
  @validator('anomalyresult')
  def anomalyresult_validate(cls, v):
    if type(v) is not int:
      raise ValueError(f'{v} must be int')
    return v
