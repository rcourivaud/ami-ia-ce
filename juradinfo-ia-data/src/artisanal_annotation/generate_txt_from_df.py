#!/usr/bin/env python 
#-*- coding: utf-8 -*-

"""
Created on 2020/07/13

Select n texts from ocr results table and write it to txt file

@author: jassu-ondo
"""

import sys
import os
from pathlib import Path
import pandas as pd
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from base.db import DataBase
db = DataBase.initialize()
engine = db["engine"]

db_app_data_tab = 'app_requetes'
OUTPUT_FOLDER = Path("C:\\Users\\jassu-ondo\\Documents\\projet_juradinfo_ia\\data\\artifical_annotation")
init_num = 200

# read data
df_requetes = pd.read_sql("select request_name, content from {} order by rand() limit 100".format(db_app_data_tab), engine).reset_index(drop=True)

# export to txt
for i in df_requetes.index:
    file_name = str(init_num+i) + '_' + df_requetes['request_name'][i] + '.txt'
    txt = df_requetes['content'][i].replace("###", "\n")
    with open(os.path.join(OUTPUT_FOLDER, file_name), 'w') as txt_file:
	    txt_file.write(txt)
	