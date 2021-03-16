from scipy import stats
import numpy as np
import spacy
import oseti
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# 不快係数
def hukai_calc(temp, humid):
  hukai = 0.81 * temp + humid * 0.01 * (0.99 * temp - 14.3) + 46.3
  return hukai

# 乾燥係数
def kanso_calc(humid):
  # Saturated Water Vapor Amount                                
  # http://es.ris.ac.jp/~nakagawa/met_cal/satu_vapor.html
  # SWVA at inroom temperature 20C is 17.31 g/m^3
  swva = 17.31
  kanso = swva * humid / 17
  return kanso

# 固有表現抽出
def ne2string(text, lang):
  if lang == "en":
    nlp = spacy.load('en_core_web_md')
  elif lang == "fr":
    nlp = spacy.load('fr_core_news_md')
  elif lang == "zh":
    nlp = spacy.load('zh_core_web_md')
  else:
    nlp = spacy.load('ja_ginza')
  nes = set([ent.text for ent in nlp(text).ents])
  ne_string = " ".join(nes)
  return ne_string

# SentimentAnalysis
def sent2score(text, lang):
  if lang == "en":
    analyzer = SentimentIntensityAnalyzer()
    sent_score = analyzer.polarity_scores(text)["compound"]
  else:
    analyzer = oseti.Analyzer()
    sent_score = np.mean(analyzer.analyze(text))
  return float(sent_score)

# ホテリング理論
def hotelling(value, model):
  mean = model['mean']
  variance = model['variance']
  anomaly_score = (value - mean)**2 / variance
  threshold = stats.chi2.interval(0.99, 1)[1]
  if anomaly_score > threshold:
    # 異常
    anomalyresult = -1
  else:
      # 正常
    anomalyresult = 1
  return anomaly_score, threshold, anomalyresult
