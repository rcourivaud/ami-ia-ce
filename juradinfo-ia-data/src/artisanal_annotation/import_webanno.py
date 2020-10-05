import json
import os
from pathlib import Path
import pickle

##########
# params #
##########
data_dir = "C:/Users/jassu-ondo/Documents/projet_juradinfo_ia/data/artificial_annotation/annotation_artisanale"
##############
# end params #
##############

# functions 
def extract_idx(lst_labels, data):
    
    list_res = []
    for label in  lst_labels:
        if label in data["_views"]['_InitialView']:
            for idx in data["_views"]['_InitialView'][label]:
                list_res.append(idx)
    #return  [idx for label in  lst_labels for idx in data["_views"]['_InitialView'][label] ]
    return list_res

def extract_NE(idx, data):
    dct = data['_referenced_fss'][str(idx)]
    dct_NE = {}
    dct_NE["sofa"] = dct["sofa"]
    dct_NE["begin"] = dct["begin"]
    dct_NE["end"] = dct["end"]
    dct_NE["value"] = dct["_type"][:-4]
    return dct_NE

def lst_NEs(lst_idx, data):
    lst_NE = []
    for idx in lst_idx:
        lst_NE.append(extract_NE(idx, data))
    return lst_NE

def lst_sentences(sentence, data):
    return [data['_referenced_fss']['12']['sofaString'][dct['begin']:(dct['end'] + 1)] for dct in sentence]

##############
# begin code #
##############

lst_labels = ['D_faitLink', 'D_moyenLink', 'D_conclusionLink', 'F_faitLink', 'F_moyenLink', 'F_conclusionLink']

list_files = []
for folder in os.listdir(Path(data_dir)):
    for f in os.listdir(os.path.join(data_dir,folder)):
        if f.split(".")[-1] == "json":
            list_files.append(os.path.join(data_dir,folder,f))

# create spacy data formatting
SPACY_DATA = []
list_ent = []
for file in list_files:
    with open(file, encoding='utf-8') as data_file:
        data = json.load(data_file)
    
    # initial text document
    text_doc = data['_referenced_fss']['12']['sofaString']
    
    # Extract entity start/end postions and names
    lst_idx = extract_idx(lst_labels, data)
    ent_loc = lst_NEs(lst_idx, data)
    
    dict_entities = {'entities':[]}
    for ent in ent_loc:
        dict_entities['entities'].append((ent['begin'], ent['end'], ent['value']))
        list_ent.append(ent['value'])
        list_ent = list(set(list_ent))
    SPACY_DATA.append((text_doc, dict_entities))
    
    
# transform annotation to match only fait, moyen, conclusion
SPACY_DATA_v2 = []
list_ent_v2 = []
for anno in SPACY_DATA:
    text_doc = anno[0]
    dict_entities = {'entities':[]}
    try:
        fait_start = [line for line in anno[1]['entities'] if line[2]=='D_fait'][0][0]
        fait_end = [line for line in anno[1]['entities'] if line[2]=='F_fait'][0][1]
        dict_entities['entities'].append((fait_start, fait_end, 'fait'))
    except:
        continue
    try:    
        moyen_start = [line for line in anno[1]['entities'] if line[2]=='D_moyen'][0][0]
        moyen_end = [line for line in anno[1]['entities'] if line[2]=='F_moyen'][0][1]
        dict_entities['entities'].append((moyen_start, moyen_end, 'moyen'))
    except:
        continue
    try:
        conclusion_start = [line for line in anno[1]['entities'] if line[2]=='D_conclusion'][0][0]
        conclusion_end = [line for line in anno[1]['entities'] if line[2]=='F_conclusion'][0][1]
        dict_entities['entities'].append((conclusion_start, conclusion_end, 'conclusion'))
    except:
        continue
    SPACY_DATA_v2.append((text_doc, dict_entities))
list_ent_v2 = ['fait', 'moyen', 'conclusion']
    
# save SPACY formated data
with open(os.path.join(data_dir, 'SPACY_DATA_v1.pkl'), 'wb') as f:
    pickle.dump(SPACY_DATA, f)
with open(os.path.join(data_dir, 'SPACY_DATA_v2.pkl'), 'wb') as f:
    pickle.dump(SPACY_DATA_v2, f)
    