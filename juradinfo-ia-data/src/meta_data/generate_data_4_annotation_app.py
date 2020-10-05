#!/usr/bin/env python 
#-*- coding: utf-8 -*-

"""
Created on 2020/06/25

Generate data that will be displayed by the annotation web app.

@author: jassu-ondo
"""

import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from sqlalchemy.dialects.mysql import MEDIUMTEXT
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from base.db import DataBase

db = DataBase.initialize()
engine = db["engine"]
chunk_size = 5000

#################
# PARAMS TO SET #
#################
db_all_data_tab = "gld_pipeline_results"
db_app_data_tab = 'test_requetes_meta_data'
db_app_annotation = 'app_annotation'
nb_rows = 5000
#################
# END PARAMS    #
#################

print('''
###################################
# selecting series not scan files #
###################################
''')
query_select_series = """
	SELECT CONCAT(num_dossier, '_', ta_code) AS request_id, num_dossier, ta, ta_code, request_name,
		date_enreg, content, matiere, titre, tete_serie, num_serie, nom_serie, file_path, nb_pages, 
		is_scan, fichier_meta_donnee_CE, 0 AS statut_annotation
	FROM {}
	WHERE is_scan=0 AND num_serie IS NOT NULL AND num_serie <>""
	ORDER BY RAND()
""".format(db_all_data_tab)
df_series = pd.read_sql(query_select_series, engine).reset_index(drop=True)
print('nb files selected:', df_series.shape[0])

print('''
######################################
# selecting not serie not scan files #
######################################
''')
nb_rows_not_serie = nb_rows - df_series.shape[0]
print('nb files to select:', nb_rows_not_serie)
query_select_not_series = """
	SELECT CONCAT(num_dossier, '_', ta_code) AS request_id, num_dossier, ta, ta_code, request_name,
		date_enreg, content, matiere, titre, tete_serie, num_serie, nom_serie, file_path, nb_pages, 
		is_scan, fichier_meta_donnee_CE, 0 AS statut_annotation, CONCAT(ta_code, '_', matiere) AS ta_matiere
	FROM {}
	WHERE is_scan=0 AND num_serie IS NULL OR num_serie =""
	ORDER BY RAND()
""".format(db_all_data_tab)
df_not_series = pd.read_sql(query_select_not_series, engine).reset_index(drop=True)
# sampling by ta_matier
dict_sample_dict = dict(df_not_series['ta_matiere'].value_counts(normalize=True))
df_not_series = pd.concat([df_not_series[df_not_series['ta_matiere']==k].sample(int(np.ceil(v*nb_rows_not_serie)), replace=False) for k,v in dict_sample_dict.items()], ignore_index=True)
df_not_series = df_not_series.drop('ta_matiere', axis=1)[0:nb_rows_not_serie]
print('nb files selected:', df_not_series.shape[0])
print('  using the following distribution (100 first values displayed)')
print(list(dict_sample_dict.items())[:100])

print('''
###########################
# final data frame export #
###########################
''')
df_final = pd.concat([df_series, df_not_series], ignore_index=True).sample(frac=1, replace=False).reset_index(drop=True)
df_final.to_sql(db_app_data_tab, engine, if_exists="replace", index=True, chunksize=chunk_size,
                dtype={'content': MEDIUMTEXT})
print('nb rows exported:', df_final.shape[0])

print('''
#####################################
# delete data from annotation table #
#####################################
''')
with engine.connect() as con:
	con.execute("DELETE FROM {};".format(db_app_annotation))
	