import os
from pathlib import Path
import pickle
import datetime as dt
import copy

import random
random.seed(30)
import spacy
from spacy.util import minibatch, compounding

##########
# params #
##########
data_dir = "C:/Users/jassu-ondo/Documents/projet_juradinfo_ia/data/artificial_annotation/annotation_artisanale"
model_version = 'v1'
models_dir = "C:/Users/jassu-ondo/Documents/projet_juradinfo_ia/models/annotation_artisanale/models_"+model_version

n_iter = 10
drop_rate = 0.3
train_test_split = 0.85
##############
# end params #
##############

def overlap(pos_1, pos_2):
    """
    Tell if pos 1 (start,end)  overlap pos 2 (start,end).
    ===========
    PARAMETERS
        pos_1 : a n-tuple where the two first elements are start position and end position
        pos_2 : a n-tuple where the two first elements are start position and end position
    ============
    Return a boolean
    """
    one_inside_two = pos_1[0] >= pos_2[0] and pos_1[1] <= pos_2[1]
    one_contains_two = pos_1[0] <= pos_2[0] and pos_1[1] >= pos_2[1]
    one_left_overlap_two = pos_1[0]<=pos_2[0] and pos_1[1] >= pos_2[0]
    one_righ_overlap_two = pos_1[0]<=pos_2[1] and pos_1[1] >= pos_2[1]
    overlap = one_inside_two or one_contains_two or one_left_overlap_two or one_righ_overlap_two
    return overlap

def overlap_one_in_list(pos, list_pos):
    '''
    Tell wether pos (start, end) overlap at least one of the pos inside list_pos
    Return a boolean
    '''
    is_overlapping = False
    for pos_i in list_pos:
        is_overlapping =  overlap(pos, pos_i)
        if is_overlapping:
            break
    return is_overlapping  

def drop_overlapping_annotations(data_set):
    '''
    For an entry of the data set (a paragraph and all the entities), 
    remove all entities that overlap others. For each overlapping, keep the first occurence
    =====================
    PARAMETERS
    data_set : Spacy formatted data for NER task. 
        All annotations in a paragraph must be sorted by (start,end).
    '''
    print('*drop overlapping annotations (keep first occurences)')
    t0 = dt.datetime.now()
    data_set_res = copy.deepcopy(data_set)
    nb_annotations_init = 0
    nb_annotations_kept = 0
    for i in range(len(data_set_res)): # iterate over paragraph annotated
        entry = data_set_res[i]     
        '''
        print(entry)
        print("i:", i)
        print("")
        '''
        nb_annotations_init += len(entry[1]['entities'])
        # keep annotations that doesn't overlap kept ones
        if len(entry[1]['entities']) != 0:
            list_kept_annotations = [entry[1]['entities'][0]] # initialize with the first annotation inside the paragraph 
            for i in range(1,len(entry[1]['entities'])):
                annotation_current = entry[1]['entities'][i]
                if not overlap_one_in_list(annotation_current, list_kept_annotations):
                    list_kept_annotations.append(annotation_current)
            nb_annotations_kept += len(list_kept_annotations)
            entry[1]['entities'] = list_kept_annotations
    print("")
    print('--nb initial annotations:', nb_annotations_init)
    print('--nb dropped annotations:', nb_annotations_init - nb_annotations_kept)
    print("*elapsed time (in min):", (dt.datetime.now()-t0).total_seconds()/60)
    return data_set_res

# load spacy formated data 
with open(os.path.join(data_dir, 'SPACY_DATA_'+model_version+'.pkl'), 'rb') as f:
    SPACY_DATA = pickle.load(f)
SPACY_DATA = drop_overlapping_annotations(SPACY_DATA)

cut = int(train_test_split*len(SPACY_DATA))
DATA_TRAIN = SPACY_DATA[:cut]
DATA_TEST = SPACY_DATA[cut:]

with open(os.path.join(data_dir, 'SPACY_DATA_TRAIN_'+model_version+'.pkl'), 'wb') as f:
    pickle.dump(DATA_TRAIN, f)
with open(os.path.join(data_dir, 'SPACY_DATA_TEST_'+model_version+'.pkl'), 'wb') as f:
    pickle.dump(DATA_TEST, f)

# train the ner model
t00 = dt.datetime.now()
nlp = spacy.blank('fr')  # create blank Language class
ner = nlp.create_pipe('ner')
nlp.add_pipe(ner)
LABEL = [] # labels
for _, annotations in DATA_TRAIN:
    for ent in annotations.get("entities"):
        LABEL.append(ent[2])
LABEL = list((set(LABEL)))
print('  Entities to learn :', LABEL)
for l in LABEL: # Add new entity labels to entity recognizer
    ner.add_label(l)
optimizer = nlp.begin_training() # Inititalizing optimizer
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    for itn in range(n_iter):
        t0 = dt.datetime.now()
        print('-- iteration', itn)
        random.shuffle(DATA_TRAIN)
        losses = {}
        batches = minibatch(DATA_TRAIN, size=compounding(4., 32., 1.001))
        for batch in batches:
            texts, annotations = zip(*batch) 
            # Updating the weights
            nlp.update(texts, annotations, sgd=optimizer, drop=drop_rate, losses=losses)
        print('Losses', losses)
        print('-- elapsed time (in min)', (dt.datetime.now()-t0).total_seconds()/60)

# Save the model
ner_model_name = 'spacy_ner_niter_'+str(n_iter)+'_droprate_'+str(drop_rate)
ner_model_path = os.path.join(models_dir, ner_model_name)
#if not ner_model_dir.exists():
#    ner_model_dir.mkdir()
nlp.meta['name'] = ner_model_name
nlp.to_disk(ner_model_path)
print("Saved model to", ner_model_path)
training_time = round((dt.datetime.now()-t00).total_seconds()/60,2)
print("# train and save NER model - elapsed time (in min):", training_time)
            