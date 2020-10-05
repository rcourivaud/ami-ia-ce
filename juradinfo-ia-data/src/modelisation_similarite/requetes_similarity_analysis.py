# -*- coding: utf-8 -*-
"""
Created on 2020/07/23

get the most similar documents of given input document

@author: jassu-ondo
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from pathlib import Path
import pandas as pd
from datetime import datetime
from elasticsearch import Elasticsearch
from wordcloud import WordCloud
import utils_text_similarity as utils

from sqlalchemy import create_engine
db_uri = "{dialecte}://{username}:{password}@{hostname}/{databasename}".format(
            dialecte="mysql+pymysql",
            username="ocr",
            password="CE001!@",
            hostname="127.0.0.1:3306",
            databasename="requests_db")
engine = create_engine(db_uri)

es = Elasticsearch(timeout=300)
wc = WordCloud(background_color="white", max_words=1500, width = 600, height = 600) # word cloud chart
        
##########
# params #
##########
folder_output_analysis = Path("C:/Users/jassu-ondo/Documents/projet_juradinfo_ia/data/analys_similarite")
db_requetes_tab = "gld_requetes_reduites"
index_name = "index_requetes_2"
max_similar_docs = 100
max_requetes_to_analyze_by_serie = 5
##########
# params #
##########

# functions definition
def generate_word_cloud(folder_path, word_cloud_file_name, es, index_name, request_name):
    requete_image_file_path = os.path.join(folder_path, word_cloud_file_name)
    tv_dict = es.termvectors(index=index_name, id=request_name, fields='content_reduced', term_statistics=True, 
                   field_statistics=False, positions=False)['term_vectors']['content_reduced']['terms']
    tv_dict = {k: tv_dict[k]['term_freq']/tv_dict[k]['doc_freq'] for k in tv_dict}
    wc.generate_from_frequencies(tv_dict)
    wc.to_file(requete_image_file_path)

# get requetes and num series, to retrieve in index
sql_query = """
SELECT request_name,
        CASE 
            WHEN num_serie IS NULL OR num_serie="" THEN "Pas série" 
            ELSE num_serie 
        END AS num_serie
FROM {}
ORDER BY RAND()""".format(db_requetes_tab)
df_requetes = pd.read_sql(sql_query, con=engine)

# get distinct num_serie
list_num_serie = df_requetes['num_serie'].unique()

# do word cloud inside each serie
for num_serie in list_num_serie[8:]:
    print("\nAnalysing serie:", num_serie)
    serie_folder_path = os.path.join(folder_output_analysis, num_serie)
    
    df_requetes_filtered = df_requetes.loc[df_requetes['num_serie']==num_serie].reset_index(drop=True)
    
    nb_req_max = min(max_requetes_to_analyze_by_serie, df_requetes_filtered.shape[0])
    
    # some requete analysis
    for i in range(nb_req_max):
        request_name = df_requetes_filtered['request_name'][i]
        print("-- requete:", request_name)
        
        requete_folder_path = os.path.join(serie_folder_path, request_name)
        if not Path(requete_folder_path).exists():
            Path(requete_folder_path).mkdir(parents=True)
        
        # generate this requete word cloud
        word_cloud_file_name = "sim_0_"+(num_serie+'_'+request_name)[0:50]+".png"
        try:
            generate_word_cloud(requete_folder_path, word_cloud_file_name, es, index_name, request_name)
        except:
            print("    word cloud not generated because of content_reduced absence/problem")
            next
        # get most similar requetes
        results = es.search(index=index_name, size=max_similar_docs, body={
            "query": {
                "more_like_this": {
                    "fields": ["content_reduced"],
                    "like": {
                        "_id": request_name
                    }
                }
            }    
        })['hits']['hits']
        
        for j in range(len(results)):
            requete_j_id = results[j]['_id']
            print("    similar requete:", requete_j_id)
            requete_j_num_serie = results[j]['_source']['num_serie']
            requete_j_word_cloud_file_name = "sim_"+str(j+1)+"_"+(requete_j_num_serie+'_'+requete_j_id)[0:50]+".png"
            generate_word_cloud(requete_folder_path, requete_j_word_cloud_file_name, es, index_name, requete_j_id)
        
        
        
        