import os
from pathlib import Path
import pickle
import datetime as dt

import pandas as pd
import random
random.seed(30)
from random import shuffle
import spacy
from spacy import displacy

##########
# params #
##########
data_dir = "C:/Users/jassu-ondo/Documents/projet_juradinfo_ia/data/artificial_annotation/annotation_artisanale"
model_version = 'v1'
models_dir = "C:/Users/jassu-ondo/Documents/projet_juradinfo_ia/models/annotation_artisanale/models_"+model_version
ner_model_name = "spacy_ner_niter_10_droprate_0.3"
dataviz_dir = "C:/Users/jassu-ondo/Documents/projet_juradinfo_ia/data/artificial_annotation/html_dataviz/html_dataviz_"+model_version
##########
# params #
##########

# load ner model
ner_model = spacy.load(os.path.join(models_dir, ner_model_name))

# visualize train data in html

DATA_TRAIN = pd.read_pickle(os.path.join(data_dir, 'SPACY_DATA_TRAIN_'+model_version+'.pkl'))
shuffle(DATA_TRAIN) # to ensure that we display the variety of annotations
html_dataviz_dir = os.path.join(dataviz_dir, ner_model_name, 'train')
if not Path(html_dataviz_dir).exists():
    Path(html_dataviz_dir).mkdir(parents=True)
i = 0
while i <20 and i < len(DATA_TRAIN): # display only 20 documents
    text_i, ents_i = DATA_TRAIN[i]
    # original data
    original_data = {'text': text_i, 'ents':[], 'title':'original entities'}
    for ent in ents_i['entities']:
        original_data['ents'].append({'start':ent[0], 'end':ent[1], 'label':ent[2]})
    html_txt = displacy.render([original_data], style="ent", jupyter=False, manual=True)
    html_path = os.path.join(html_dataviz_dir, 'requete_'+str(i)+'_train_original_entities.html')
    with open(html_path, 'w') as file:
        file.write(html_txt)
    # prediction data
    doc_pred = ner_model(text_i)
    pred_data = {'text':text_i, 'ents':[], 'title':'predicted entities'}
    for ent in doc_pred.ents:
        if 'fait' in ent.label_.lower():
            continue
        pred_data['ents'].append({'start':ent.start_char, 'end':ent.end_char, 'label':ent.label_})
    html_txt = displacy.render([pred_data], style="ent", jupyter=False, manual=True)
    html_path = os.path.join(html_dataviz_dir, 'requete_'+str(i)+'_train_prediction_entities.html')
    with open(html_path, 'w') as file:
        file.write(html_txt)
    i+=1

# visualize test data in html

DATA_TEST = pd.read_pickle(os.path.join(data_dir, 'SPACY_DATA_TEST_'+model_version+'.pkl'))
shuffle(DATA_TRAIN) # to ensure that we display the variety of annotations
html_dataviz_dir = os.path.join(dataviz_dir, ner_model_name, 'test')
if not Path(html_dataviz_dir).exists():
    Path(html_dataviz_dir).mkdir(parents=True)
i = 0
while i <20 and i < len(DATA_TEST): # display only 20 documents
    text_i, ents_i = DATA_TEST[i]    
    doc_pred = ner_model(text_i)
    pred_data = {'text':text_i, 'ents':[], 'title':'predicted entities'}
    for ent in doc_pred.ents:
        pred_data['ents'].append({'start':ent.start_char, 'end':ent.end_char, 'label':ent.label_})
    html_txt = displacy.render([pred_data], style="ent", jupyter=False, manual=True)
    html_path = os.path.join(html_dataviz_dir, 'requete_'+str(i)+'_test_prediction_entities.html')
    with open(html_path, 'w') as file:
        file.write(html_txt)
    i+=1    