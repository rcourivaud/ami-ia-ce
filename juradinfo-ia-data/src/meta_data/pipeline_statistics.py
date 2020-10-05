#!/usr/bin/env python 
#-*- coding: utf-8 -*-

"""
Created on 2020/09/10

Get statistics about the pipeline result table

@author: jassu-ondo
"""


import sys
import os
from pathlib import Path
import datetime as dt
import pandas as pd
import re
from openpyxl import load_workbook
from sqlalchemy.dialects.mysql import MEDIUMTEXT
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from base.db import DataBase

db = DataBase.initialize()
engine = db["engine"]

#################
# PARAMS TO SET #
#################
db_pipeline_result_table = 'gld_pipeline_results'
db_ocr_result_serie_table = 'tmp_ocr_series'
db_ocr_result_vrac_table = 'tmp_ocr_test'

dict_stats_file = {'file_path':r"X:\TC inter-services\Juradinfo IA\analyses\meta_data\pipeline_analyse.xlsx", 
                   'stats_sheet':'Stats_brutes',
                   'meta_data_ko_sheet':'Requêtes_sans_meta_données',
                   'serie_distrib_sheet':'Répartition_séries_rattachées'}
#################
# END PARAMS    #
#################

print("""
1 - Import data from database""")
      
sql_query = """SELECT num_dossier, ta_code, request_name, file_path, num_serie_normalise, is_scan 
                FROM {}""".format(db_pipeline_result_table)
df_pipeline_results = pd.read_sql(sql_query, engine)
df_pipeline_results['dossier']= df_pipeline_results['file_path'].apply(lambda x: x.split('/')[-2])

sql_query = """SELECT CAST(num_folder AS CHAR) as num_dossier, ta as ta_code, request_name, file_path, is_scan
                FROM {}
        UNION 
                SELECT CAST(num_folder AS CHAR) as num_dossier, ta as ta_code, request_name, file_path, is_scan
                FROM {}""".format(db_ocr_result_serie_table, db_ocr_result_vrac_table)
df_ocr_results = pd.read_sql(sql_query, engine)
df_ocr_results['dossier']= df_ocr_results['file_path'].apply(lambda x: x.split('/')[-2])

print(""""
2 - Get statistics""")

dict_analysis = {}
dict_analysis['nb_requetes_extraction_pdf_series'] = df_ocr_results['dossier'].value_counts()['Extraction_PDF_series']
dict_analysis['nb_requetes_extraction_pdf_vrac'] = df_ocr_results['dossier'].value_counts()['Extraction3_PDF_vrac']
dict_analysis['nb_requetes_extraction_pdf_series_scan'] = df_ocr_results.loc[(df_ocr_results['dossier']=='Extraction_PDF_series') & (df_ocr_results['is_scan']==1)].shape[0]
dict_analysis['nb_requetes_extraction_pdf_vrac_scan'] = df_ocr_results.loc[(df_ocr_results['dossier']=='Extraction3_PDF_vrac') & (df_ocr_results['is_scan']==1)].shape[0]

# stats without duplicates
dict_analysis['nb_requetes_extraction_pdf_series_without_duplicates'] = df_pipeline_results['dossier'].value_counts()['Extraction_PDF_series']
dict_analysis['nb_requetes_extraction_pdf_vrac_without_duplicates'] = df_pipeline_results['dossier'].value_counts()['Extraction3_PDF_vrac']
dict_analysis['nb_requetes_extraction_pdf_series_without_duplicates_scan'] = df_pipeline_results.loc[(df_pipeline_results['dossier']=='Extraction_PDF_series') & (df_pipeline_results['is_scan']==1)].shape[0]
dict_analysis['nb_requetes_extraction_pdf_vrac_without_duplicates_scan'] = df_pipeline_results.loc[(df_pipeline_results['dossier']=='Extraction3_PDF_vrac') & (df_pipeline_results['is_scan']==1)].shape[0]

# stats rattachement métadonnées
dict_analysis['nb_requetes_with_meta_data'] = df_pipeline_results.loc[(~df_pipeline_results['num_serie_normalise'].isnull())].shape[0]
dict_analysis['nb_requetes_in_serie'] = df_pipeline_results.loc[(~df_pipeline_results['num_serie_normalise'].isnull()) & (df_pipeline_results['num_serie_normalise']!="")].shape[0]

df_analysis = pd.DataFrame.from_dict(dict_analysis, orient='index')
df_analysis.columns=['stats']

print("""
3 - Get requetes without meta_data""")
df_tmp_ko_requetes = df_pipeline_results.loc[df_pipeline_results['num_serie_normalise'].isnull(), ['num_dossier', 'ta_code']]
df_requetes_meta_data_ko = pd.DataFrame(columns=['nom_fichier', 'dossier'])
for i in df_tmp_ko_requetes.index:
    tmp_num_dossier = df_tmp_ko_requetes.loc[i, 'num_dossier']
    tmp_ta_code = df_tmp_ko_requetes.loc[i, 'ta_code']
    df_tmp = df_ocr_results.loc[(df_ocr_results['num_dossier']==tmp_num_dossier) & (df_ocr_results['ta_code']==tmp_ta_code), ['file_path', 'dossier']]
    df_tmp['nom_fichier'] = df_tmp['file_path'].apply(lambda x: x.split('/')[-1])
    df_requetes_meta_data_ko = df_requetes_meta_data_ko.append(df_tmp[['nom_fichier', 'dossier']], ignore_index=True)

print("""
4 - Get series distribution""")
series_distribution = df_pipeline_results['num_serie_normalise'].value_counts()
series_distribution = series_distribution.rename_axis('num_serie_normalise').reset_index(name='nb_requetes')

print("""
5 - Export Excel""")
book = load_workbook(dict_stats_file['file_path'])
writer = pd.ExcelWriter(dict_stats_file['file_path'], engine = 'openpyxl')
writer.book = book

std=book.get_sheet_by_name(dict_stats_file['stats_sheet'])
book.remove_sheet(std)
df_analysis.to_excel(writer, sheet_name = dict_stats_file['stats_sheet'])

std=book.get_sheet_by_name(dict_stats_file['meta_data_ko_sheet'])
book.remove_sheet(std)
df_requetes_meta_data_ko.to_excel(writer, sheet_name = dict_stats_file['meta_data_ko_sheet'], index=False)

std=book.get_sheet_by_name(dict_stats_file['serie_distrib_sheet'])
book.remove_sheet(std)
series_distribution.to_excel(writer, sheet_name = dict_stats_file['serie_distrib_sheet'], index=False)

writer.save()
writer.close()
 