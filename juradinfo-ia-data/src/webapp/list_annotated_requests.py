#!/usr/bin/env python 
#-*- coding: utf-8 -*-

"""
Created on 2020/09/15

Get list of annotated requests with their TA

@author: jassu-ondo
"""


import sys
import os
from pathlib import Path
import datetime as dt
import pandas as pd
import re
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from base.db import DataBase

db = DataBase.initialize()
engine = db["engine"]

#################
# PARAMS TO SET #
#################
db_app_requetes_tab = "test_requetes_meta_data"
data_out_file = "X:/TC inter-services/Juradinfo IA/analyses/phase_annotation/requetes_annotees.xlsx"
#################
# END PARAMS    #
#################

sql_query = """
SELECT request_id as id_requete, num_dossier, ta, ta_code, num_serie, matiere, titre, 
    DATE(date_enreg) as date_enreg, file_path as chemin_fichier
FROM {} WHERE statut_annotation=1
""".format(db_app_requetes_tab)

df_requetes_annotees = pd.read_sql(sql_query, engine).reset_index(drop=True)

df_requetes_annotees.to_excel(data_out_file, index=False)