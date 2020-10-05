#!/usr/bin/env python 
#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
import pandas as pd
import os

db_uri = "{dialecte}://{username}:{password}@{hostname}/{databasename}".format(
            dialecte="mysql+pymysql",
            username="to_be_set",
            password="to_be_set",
            hostname="to_be_set",
            databasename="to_be_set")
engine = create_engine(db_uri)


##########
# params #
db_app_annotation_tab = "app_annotation"
data_outt_folder = "/home/jassu-ondo/juradinfo_ia_data/data_out"
result_file_name = "nb_requetes_annotees_user.csv"
##############
# end params #
##############

sql_query = """
SELECT username, count(distinct request_id) AS nb_requetes_annotees 
FROM {} group by username
""".format(db_app_annotation_tab)
df_nb_requetes_user = pd.read_sql(sql_query, engine).reset_index(drop=True)
df_nb_requetes_user.to_csv(os.path.join(data_outt_folder, result_file_name), sep=",", index=False, encoding='utf-8')
