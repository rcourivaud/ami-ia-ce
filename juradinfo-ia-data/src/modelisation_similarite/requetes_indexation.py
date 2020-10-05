# -*- coding: utf-8 -*-
"""
Created on 2020/07/21

import requests from the database and index it in elasticsearch

@author: jassu-ondo
"""

import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from base.db import DataBase


db = DataBase.initialize()
engine = db["engine"]
chunk_size = 5000

from sqlalchemy import create_engine
db_uri = "{dialecte}://{username}:{password}@{hostname}/{databasename}".format(
            dialecte="mysql+pymysql",
            username="ocr",
            password="CE001!@",
            hostname="127.0.0.1:3306",
            databasename="requests_db")
engine = create_engine(db_uri)


##########
# params #
##########
db_requetes_tab = "gld_requetes_reduites"
index_name = "index_requetes_2"
##########
# params #
##########

# import data from the database
sql_query = "SELECT * FROM {}".format(db_requetes_tab)
df_requetes = pd.read_sql(sql_query, con=engine)
cols_2_keep = ['request_name', 'matiere', 'ta_code', 'nb_pages', 'content',
       'pos_start', 'pos_fin', 'num_serie']
df_requetes = df_requetes[cols_2_keep]
df_requetes['num_serie'] = df_requetes['num_serie'].fillna('Absence meta données')
df_requetes['num_serie'] = df_requetes['num_serie'].replace(r'^\s*$', 'Pas série', regex=True)
for field in ['matiere', 'ta_code']:
    df_requetes[field] = df_requetes[field].fillna('Non renseigné')
df_requetes['nb_pages'] = df_requetes['nb_pages'].fillna(0)
df_requetes['content_reduced'] = df_requetes.apply(lambda x: x["content"][min(x["pos_start"], x["pos_fin"]):max(x["pos_start"], x["pos_fin"])], axis=1)

############
# indexing #
############

# mapping
analyzer = {
  "settings": {
    "analysis": {
      "filter": {
        "french_elision": {
          "type": "elision",
          "articles_case": "true",
          "articles": ["l", "m", "t", "qu", "n", "s",
              "j", "d", "c", "jusqu", "quoiqu",
              "lorsqu", "puisqu"]
        },
        "french_stop": {
          "type": "stop",
          "stopwords":  "_french_" 
        },
        "french_stemmer": {
          "type": "stemmer",
          "language": "light_french"
        }
      },
      "analyzer": {
        "rebuilt_french": {
          "tokenizer":  "standard",
          "filter": ["french_elision", "lowercase", "french_stop", "french_stemmer"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "matiere": {"type": "text"},
      "ta_code": {"type": "text"},
      "nb_pages": { "type": "integer"},
      "num_serie": {"type": "text"},
      "content_reduced":{"type": "text", "analyzer": "rebuilt_french"}
    }
  }
}

# creation index
es = Elasticsearch(timeout=300)
#es.indices.delete(index=index_name)
es.indices.create(index=index_name, body=analyzer)

# indexation

key_field = "request_name"
indexed_fileds =['matiere', 'ta_code', 'nb_pages', "num_serie", 'content_reduced']

def filterKeys(document):
    return {key: document[key] for key in indexed_fileds }

def doc_generator(df):
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield {
                "_index": index_name,
                "_id" : f"{document[key_field]}",
                "_source": filterKeys(document),
            }
    #raise StopIteration
    
helpers.bulk(es, doc_generator(df_requetes))
