#!/usr/bin/env python 
#-*- coding: utf-8 -*-

"""
Created on 2020/06/24

Agregate from the database meta-data to the ocr results table.

@author: jassu-ondo
"""

import sys
import os
from pathlib import Path
import datetime as dt
import pandas as pd
import re
from sqlalchemy.dialects.mysql import MEDIUMTEXT
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from base.db import DataBase

db = DataBase.initialize()
engine = db["engine"]
chunk_size = 5000
CHAR_MAX_LENGTH = 10000000

#################
# PARAMS TO SET #
#################

list_db_ocr_results_table = ['tmp_ocr_series', 'tmp_ocr_test']
db_meta_data_table = 'gld_meta_data_requetes'
db_output_table = 'gld_pipeline_results2'
#################
# END PARAMS    #
#################

print("""
###############################################
# 1 - select data from all ocr_results tables #
###############################################
""")

df_ocr_results = pd.DataFrame(columns = ['num_dossier', 'ta_code', 'content', 'request_name', 
                                         'file_path', 'nb_pages', 'is_scan'])
for tab in list_db_ocr_results_table:
    sql_query = """SELECT CAST(num_folder AS CHAR) as num_dossier, ta as ta_code, content, 
                	request_name, file_path, page_number as nb_pages, is_scan
                FROM {}""".format(tab)
    df_current = pd.read_sql(sql_query, engine)
    df_ocr_results = df_ocr_results.append(df_current, ignore_index=True)
df_ocr_results = df_ocr_results.drop_duplicates(['num_dossier', 'ta_code'])

print("""
######################
# 2 - join meta-data #
######################
""")

sql_query = """SELECT num_dossier, ta_code, ta, date_enreg, matiere, titre, tete_serie, 
                    num_serie_normalise, num_serie, nom_serie, fichier_meta_donnee_CE
                FROM {}""".format(db_meta_data_table)
df_meta_data = pd.read_sql(sql_query, engine)

df_pipeline_results = pd.merge(df_ocr_results, df_meta_data, on=['num_dossier', 'ta_code'], how='left')
list_cols_ordered = ['num_dossier', 'ta_code', 'ta', 'date_enreg', 'content', 'matiere', 'titre', 'tete_serie', 
                     'num_serie_normalise', 'num_serie', 'nom_serie','request_name', 'file_path', 'nb_pages', 'is_scan','fichier_meta_donnee_CE']
df_pipeline_results = df_pipeline_results[list_cols_ordered]

print("""
#############################
# 3 - add-on post treatment #
#############################
""")
# In mysql 5.5, no REGEXP_REPLACE function ==> So we do that treatment in python
df_pipeline_results['content'] = df_pipeline_results['content'].apply(lambda x: re.sub(r"page [0-9]+ sur [0-9]+", "", x, flags=re.IGNORECASE))
df_pipeline_results['content'] = df_pipeline_results['content'].str.strip('###').apply(lambda x : re.sub(r" +###", "###", x)).apply(lambda x : re.sub(r"### +", "###", x))

print("""
#################
# export to bdd #
#################
""")
# rename old table before writting
str_datetime = dt.datetime.now().strftime("%Y%m%d%H%M%S")
db_output_table_old = db_output_table+'_'+str_datetime
with engine.connect() as con:
    con.execute("""ALTER TABLE {} RENAME {}""".format(db_output_table, db_output_table_old))

df_pipeline_results.to_sql(db_output_table, engine, if_exists="replace", index=True, chunksize=chunk_size,
                dtype={'content': MEDIUMTEXT})