#!/usr/bin/env python 
#-*- coding: utf-8 -*-

"""
Created on Thu Jun 11 19:07:59 2020

Write meta-data related to series requetes and vrac requetes to the database

@author: jassu-ondo
"""

import sys
import os
from pathlib import Path
import datetime as dt
import pandas as pd
from unidecode import unidecode
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from base.db import DataBase

db = DataBase.initialize()
engine = db["engine"]
chunk_size = 5000

INPUT_FOLDER_series = Path("X:\TC inter-services\Juradinfo IA\Extraction_PDF_series")
l_files_series = ["Extraction_Séries_SkipperTA.xlsx", "2. Série LINKY.xlsx", 
                  "2. Série ASA.xlsx", "2. Série Amiante.xlsx", "2. Série 235TER CGI.xlsx"]

INPUT_FOLDER_vrac = Path("X:\TC inter-services\Juradinfo IA\Extraction3_PDF_vrac\meta_donnees")
l_files_vrac = ["Extraction3 méta-données.xlsx", "Complement.xlsx"]

file_correspondance_ta = "X:\\TC inter-services\Juradinfo IA\\tables_correspondances\correspondance_ta_code_v_202009.csv"
file_correspondance_num_serie_normalise = r"X:\TC inter-services\Juradinfo IA\tables_correspondances\correspondance_numSerie_numSerieNormalise.xlsx"

meta_data_table_db = "gld_meta_data_requetes"
meta_data_output_file = "X:\TC inter-services\Juradinfo IA\\analyses\\meta_data\\meta_data_"+dt.datetime.now().strftime("%Y_%m_%d")+".xlsx"

#####################
# some util funtions
def post_process_meta_data(df_in):
	list_col_2_strip_int = ['tete_serie']
	list_col_2_strip_str = ['num_dossier', 'ta', 'num_serie', 'nom_serie', 'matiere', 'titre']
	for col in list_col_2_strip_int:
		df_in[col] = pd.to_numeric(df_in[col], errors='coerce')
		df_in[col] = df_in[col].fillna(0).astype('int')
	for col in list_col_2_strip_str:
		df_in[col] = df_in[col].str.strip()
	df_in['ta'] = df_in['ta'].str.lower().str.strip().str.replace(' ', '')
	return df_in
	
def stats_doublons(df_in):	
	dict_stats = {}
	dict_stats['nb_row_total'] = df_in.shape[0]
	dict_stats['nb_unique_num_dossier_ta_with_doublon'] = len(df_in.loc[df_in['nb_doublons']>=2, 'num_dossier_ta'].unique())
	dict_stats['nb_num_dossier_ta_with_doublon'] = df_in.loc[df_in['nb_doublons']>=2, 'num_dossier_ta'].shape[0]
	dict_stats['nb_distinct_ta'] = len(df_in['ta'].unique())
	return dict_stats

#####################################
# 1 - read meta-data related to series
print("""
#####################################
# 1 - read meta-data related to series
""")

l_columns = ["num_dossier", "ta", "date_enreg", "tete_serie", "num_serie", "nom_serie", "matiere", "titre", "fichier_meta_donnee_CE"]
df_meta_data = pd.DataFrame(columns = l_columns)
for file_name in l_files_series:
    df_current = pd.read_excel(os.path.join(INPUT_FOLDER_series, file_name), usecols=list(range(8)), dtype=str)
    df_current["fichier_meta_donnee_CE"] = file_name
    df_current.columns = l_columns
    df_current['date_enreg'] = pd.to_datetime(df_current['date_enreg'])
    df_current = post_process_meta_data(df_current)
    df_meta_data = df_meta_data.append(df_current, ignore_index=True)
df_meta_data['num_dossier_ta'] = df_meta_data["num_dossier"].astype('str') + '_' + df_meta_data["ta"]
df_meta_data = df_meta_data[['num_dossier_ta'] + [col for col in df_meta_data.columns if col!='num_dossier_ta']]
print(df_meta_data.dtypes)

# ordonner les enregistrements par numéro de dossier croissant et date_eng decroissante
df_meta_data = df_meta_data.sort_values(["num_dossier", "date_enreg"], ascending=[True, False])
# comptage doublons (num_dossier, ta)
df_meta_data["nb_doublons"] = df_meta_data.groupby("num_dossier_ta")["num_dossier_ta"].transform('count')

# Stats doublons
dict_stats = stats_doublons(df_meta_data)
print("stats doublons")
print("  ",dict_stats)

# dataframe dédoublonnées
df_dedoublonnee_series = df_meta_data.drop_duplicates("num_dossier_ta").drop(["nb_doublons"], axis=1)

# stats dédoublonnées
df_stats_dedoublonnees = df_dedoublonnee_series['ta'].value_counts()
print("stats dédoublonnées")
print("  ", df_stats_dedoublonnees)

#####################################
# 2 - read meta-data related to vrac
print("""
#####################################
# 2 - read meta-data related to vrac
""")

l_columns_vrac = ["num_dossier", "ta", "date_enreg", "tete_serie", "num_serie", "nom_serie", "matiere", "titre", "fichier_meta_donnee_CE"]
df_meta_data_vrac = pd.DataFrame(columns = l_columns_vrac)
for file_name in l_files_vrac:
    df_current = pd.read_excel(os.path.join(INPUT_FOLDER_vrac, file_name), sheet_name="TDF-TA", usecols=list(range(8)), dtype=str)
    df_current["fichier_meta_donnee_CE"] = file_name
    df_current.columns = l_columns_vrac
    df_current['date_enreg'] = pd.to_datetime(df_current['date_enreg'])
    df_current = post_process_meta_data(df_current)
    df_meta_data_vrac = df_meta_data_vrac.append(df_current, ignore_index=True)
df_meta_data_vrac['num_dossier_ta'] = df_meta_data_vrac["num_dossier"].astype('str') + '_' + df_meta_data_vrac["ta"]
df_meta_data_vrac = df_meta_data_vrac[['num_dossier_ta'] + [col for col in df_meta_data_vrac.columns if col!='num_dossier_ta']]

# ordonner les enregistrements par numéro de dossier croissant et date_eng decroissante
df_meta_data_vrac = df_meta_data_vrac.sort_values(["num_dossier", "date_enreg"], ascending=[True, False])
# comptage doublons (num_dossier, ta)
df_meta_data_vrac["nb_doublons"] = df_meta_data_vrac.groupby("num_dossier_ta")["num_dossier_ta"].transform('count')

# stats doublons
dict_stats = stats_doublons(df_meta_data_vrac)
print("stats doublons")
print("  ",dict_stats)

# dataframe dédoublonnées
df_dedoublonnee_vrac = df_meta_data_vrac.drop_duplicates("num_dossier_ta").drop(["nb_doublons"], axis=1)

# stats dédoublonnées
df_stats_dedoublonnees = df_dedoublonnee_vrac['ta'].value_counts()
print("stats dédoublonnées")
print("  ", df_stats_dedoublonnees)

################################################
# 3 - concatenation des 2 tables series et vrac
print("""
################################################
# 3 - concatenation des 2 tables series et vrac
""")
df_meta_data_full = df_dedoublonnee_series.append(df_dedoublonnee_vrac, ignore_index=True)

# comptage doublons (num_dossier, ta)
df_meta_data_full["nb_doublons"] = df_meta_data_full.groupby("num_dossier_ta")["num_dossier_ta"].transform('count')

# stats doublons
dict_stats = stats_doublons(df_meta_data_full)
print("stats doublons")
print("  ",dict_stats)

# dataframe dédoublonnées
df_dedoublonnee_full = df_meta_data_full.drop_duplicates("num_dossier_ta").drop(["nb_doublons"], axis=1)
df_dedoublonnee_full = df_dedoublonnee_full.reset_index(drop=True)
print("df_dedoublonnee_full - nb rows :", df_dedoublonnee_full.shape[0])

##########################################
# 4 - mapping ta_code
print("""
##########################################
# 4 - mapping ta_code
""")
df_mapping_ta_code = pd.read_csv(file_correspondance_ta)[['ta', 'ta_code']]
df_mapping_ta_code['ta'] = df_mapping_ta_code["ta"].str.lower().str.strip()
df_meta_data_final = pd.merge(df_dedoublonnee_full, df_mapping_ta_code, on='ta', how='left')
l_first_cols = ['num_dossier_ta', 'num_dossier', 'ta', 'ta_code']
df_meta_data_final = df_meta_data_final[l_first_cols + [col for col in df_meta_data_final.columns if col not in l_first_cols]]

##########################################
# 5 - mapping num_serie_normalisee
print("""
##########################################
# 4 - mapping num_serie_normalisee
""")
df_num_series_normalise = pd.read_excel(file_correspondance_num_serie_normalise)
df_num_series_normalise['num_serie'] = df_num_series_normalise['num_serie'].apply(lambda x: unidecode(x).lower().strip()) 
dict_mapping = dict(df_num_series_normalise.values)
df_meta_data_final['num_serie_normalise'] = df_meta_data_final['num_serie'].apply(lambda x: unidecode(x).lower().strip()).replace(dict_mapping).str.upper()
l_first_cols = ['num_dossier_ta', 'num_dossier', 'ta', 'ta_code', 'date_enreg', 'num_serie_normalise', 'num_serie', 'nom_serie']
df_meta_data_final = df_meta_data_final[l_first_cols + [col for col in df_meta_data_final.columns if col not in l_first_cols]] 

#####################
# 5 - export to database
print("""
#####################
# 6 - export to database
""")
# rename old table before writting
str_datetime = dt.datetime.now().strftime("%Y%m%d%H%M")
meta_data_table_db_old = meta_data_table_db+'_'+str_datetime
with engine.connect() as con:
    con.execute("""ALTER TABLE {} RENAME {}""".format(meta_data_table_db, meta_data_table_db_old))
df_meta_data_final.to_sql(meta_data_table_db, engine, if_exists="replace", index=False, chunksize=chunk_size)
print("méta-données dédoublonnées exportées en BDD, table %s" %(meta_data_table_db,))

print("""
#######################################
# 7 - save table to Excel for analysis
""")
df_meta_data_final.to_excel(meta_data_output_file, index=False, engine='xlsxwriter')
