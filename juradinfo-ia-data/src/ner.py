from __future__ import unicode_literals, print_function

from base.config_reader import Config
from base.db import DataBase as db

from entities.annotation import Annotation as An
from entities.inferred_annotation import Annotation as IAn
from entities.app_requestes import Request as Rq

from sqlalchemy.sql import select

import spacy
from spacy.util import minibatch, compounding
from spacy import displacy

import random
from pathlib import Path

import datetime as dt
import copy

import os

import re
import string
import unidecode as ud
import warnings

import pandas as pd

import hashlib
import pickle

param = db.initialize()
IAn.__table__.create(bind=param["engine"], checkfirst=True)


class Data:
    """
    Class that map data form the database into NER training/testing set
    """

    def __init__(self):
        pass

    @classmethod
    def get_all_annotations(cls, engine):
        """

        :param engine: engine to execute database request
        :return: all the raws of the table app_annotation
        """
        return An.find_all(engine)

    @classmethod
    def get_text_of_request(cls, engine, rq_id):
        """
        :param engine: engine to execute database request
        :param rq_id: request id
        :return: text of the request that is saved into the table app_requetes
        """
        rows = Rq.find_by_id(engine, rq_id)
        row = next(rows)
        return row[7]

    @classmethod
    def get_distinct_request_id(cls, engine):
        """
        :param engine: engine to execute database request
        :return: distinct request id of the table app_annoation
        """
        request_ids = An.find_distinct_request_id(engine)
        lst_id = [request_id[0] for request_id in request_ids]

        return lst_id

    @classmethod
    def motif_cmpter(cls, txt, motif):
        """
        This function count the number of occurence of a motif that precede a giving position
        :param txt: the text to treat
        :param motif: the motif to count
        :return: a table that count the number of occurence to the motif depending of the position consider
        """
        n = len(txt)
        n_motif = len(motif)

        cmpt = [0] * n

        for k in range(n_motif, n, n_motif):
            if txt[(k - n_motif) : k] == motif:
                cmpt[k] = cmpt[(k - n_motif)] + 1
                for idx in range((k - n_motif), (k - 1)):
                    cmpt[idx + 1] = cmpt[idx]

        return cmpt

    @classmethod
    def update_position(cls, k, cmpt):
        """
        This function update the position that is pass to the function
        :param k: the position to update
        :param cmpt: the table used to update the positions
        :return: the updated postion
        """
        return k - (2 * cmpt[k])

    @classmethod
    def get_list_of_entities(cls, engine, rq_id, text):
        """
        This function construct the list of entities of the trainingset
        :param engine: engine to execute database request
        :param rq_id: rq_id: request id
        :param text: the text to treat
        :return: The list of entities(annotations and labels) of the text
        """
        rows = An.find_by_request_id(engine, rq_id)
        cmpt = cls.motif_cmpter(text, "###")
        lst_entities = [
            (
                cls.update_position(row[4], cmpt),
                (cls.update_position(row[5], cmpt) + 1),
                row[0],
            )
            for row in rows
        ]
        # delete duplicate
        b_set = set(tuple(x) for x in lst_entities)
        lst_entities = list(b_set)
        return lst_entities

    @classmethod
    def get_dict_entities(cls, engine, rq_id, text):
        """
        Construct a dictionnary of entities
        :param engine:  engine to execute database request
        :param rq_id: request id
        :param text: the text to treat
        :return: The dictionnary containning entities (annotations and lables)
        """
        lst_entities = cls.get_list_of_entities(engine, rq_id, text)
        d = {}
        d["entities"] = lst_entities

        return d

    @classmethod
    def idx_in_txt(cls, txt, pos, way):
        if way == -1:
            return pos >= 0
        else:
            return pos < len(txt)

    @classmethod
    def shift_idx(cls, txt, pos, way):
        aux = pos + way
        while cls.idx_in_txt(txt, aux, way):
            if txt[aux] == " " or txt[aux] == "\n" or txt[aux] in string.punctuation:
                break
            aux = aux + way

        return aux - way

    @classmethod
    def shift_lst(cls, txt, lst):

        return [
            (cls.shift_idx(txt, start, -1), cls.shift_idx(txt, end, 1), label)
            for start, end, label in lst
        ]

    @classmethod
    def get_training_chunck(cls, engine, rq_id):
        """
        Return the formated data for one request
        :param engine: engine to execute database request
        :param rq_id: request id
        :return: the formated training set for a request
        """
        text = cls.get_text_of_request(engine, rq_id)
        dct_entities = cls.get_dict_entities(engine, rq_id, text)
        text = text.replace("###", "\n")
        dct_entities["entities"] = cls.shift_lst(text, dct_entities["entities"])

        return ud.unidecode(text), dct_entities

    @classmethod
    def get_test_chunck(cls, engine, rq_id):
        """
        Return a formated request for the testing set
        :param engine: engine to execute database request
        :param rq_id:  request id
        :return: the formated testing set for a request
        """
        text = cls.get_text_of_request(engine, rq_id)
        text = text.replace("###", "\n")
        l = text.split("\n\n")

        lst_txt = [(ud.unidecode(text), {"entities": []}) for text in l]

        return lst_txt

    @classmethod
    def overlap(cls, pos_1, pos_2):
        """
        Detect overlapping annotations
        :param pos_1: start and end positions of an annotation
        :param pos_2: start and end positions of an annotation
        :return: true if they overlaped false otherwise
        """
        one_inside_two = pos_1[0] >= pos_2[0] and pos_1[1] <= pos_2[1]
        one_contains_two = pos_1[0] <= pos_2[0] and pos_1[1] >= pos_2[1]
        one_left_overlap_two = pos_1[0] <= pos_2[0] and pos_1[1] >= pos_2[0]
        one_righ_overlap_two = pos_1[0] <= pos_2[1] and pos_1[1] >= pos_2[1]
        overlap = (
            one_inside_two
            or one_contains_two
            or one_left_overlap_two
            or one_righ_overlap_two
        )
        return overlap

    @classmethod
    def overlap_one_in_list(cls, pos, list_pos):
        """
        Test if one annotation overlap with others annotations of a list
        :param pos: start and end positions of an annotation
        :param list_pos: list of annotations start and end positions
        :return: true if they overlaped false otherwise
        """
        is_overlapping = False
        for pos_i in list_pos:
            is_overlapping = cls.overlap(pos, pos_i)
            if is_overlapping:
                break
        return is_overlapping

    @classmethod
    def drop_overlapping_annotations(cls, data_set):
        """
        Delete overlapping annotations
        :param data_set: the trainingset for NER
        :return: the trainingset without overlaopping annotations
        """
        print("*drop overlapping annotations (keep first occurences)")
        t0 = dt.datetime.now()
        data_set_res = copy.deepcopy(data_set)
        nb_annotations_init = 0
        nb_annotations_kept = 0
        for i in range(len(data_set_res)):  # iterate over paragraph annotated
            entry = data_set_res[i]
            nb_annotations_init += len(entry[1]["entities"])
            # keep annotations that doesn't overlap kept ones
            if len(entry[1]["entities"]) != 0:
                list_kept_annotations = [
                    entry[1]["entities"][0]
                ]  # initialize with the first annotation inside the paragraph
                for i in range(1, len(entry[1]["entities"])):
                    annotation_current = entry[1]["entities"][i]
                    if not cls.overlap_one_in_list(
                        annotation_current, list_kept_annotations
                    ):
                        list_kept_annotations.append(annotation_current)
                nb_annotations_kept += len(list_kept_annotations)
                entry[1]["entities"] = list_kept_annotations
            data_set_res[i] = entry
        print("")
        print("--nb initial annotations:", nb_annotations_init)
        print("--nb dropped annotations:", nb_annotations_init - nb_annotations_kept)
        print("*elapsed time (in min):", (dt.datetime.now() - t0).total_seconds() / 60)
        return data_set_res

    @classmethod
    def trim_entity_spans(cls, data: list) -> list:
        """
        Remove extra space at the beginning and the end of annotations
        :param data: the NER training set
        :return: the trainingset with annotations without space
        """
        invalid_span_tokens = re.compile(r"\s")
        invalid_start = re.compile(r"[a-zA-Z]")

        cleaned_data = []
        for text, annotations in data:
            entities = annotations["entities"]
            t_aux = ud.unidecode(text)
            valid_entities = []
            for start, end, label in entities:
                valid_start = start
                valid_end = end

                while valid_start > 1 and invalid_start.match(t_aux[valid_start - 1]):
                    valid_start -= 1

                while valid_start < len(text) and invalid_span_tokens.match(
                    text[valid_start]
                ):
                    valid_start += 1

                while valid_end > 1 and invalid_span_tokens.match(text[valid_end - 1]):
                    valid_end -= 1
                valid_entities.append([valid_start, valid_end, label])
            cleaned_data.append([ud.unidecode(text), {"entities": valid_entities}])

        return cleaned_data

    @classmethod
    def get_training_set(cls, engine):
        """
        Connect to the database and get the trainingset
        :param engine: engine to execute database request
        :return: the NER training set
        """
        lst_request_id = cls.get_distinct_request_id(engine)
        tr_set = [cls.get_training_chunck(engine, rq_id) for rq_id in lst_request_id]
        tr_set = cls.trim_entity_spans(tr_set)
        tr_set = cls.drop_overlapping_annotations(tr_set)

        return tr_set

    @classmethod
    def get_testing_set(cls, engine):
        """
        Get connected to the DB and construct the testingset (request without annotations)
        :param engine: engine to execute database request
        :return: the NER testing set
        """
        lst_request_id = cls.get_list_request_id_test_set(engine)
        tst_set = [cls.get_test_chunck(engine, rq_id) for rq_id in lst_request_id]

        return tst_set, lst_request_id

    @classmethod
    def get_list_request_id_test_set(cls, engine):
        """
        Get the list of request without annotations
        :param engine:  engine to execute database request
        :return: List of request ids
        """
        request_ids = An.find_distinct_request_id(engine)
        lst_training_id = [request_id[0] for request_id in request_ids]

        all_request_ids = Rq.find_all_requests_id(engine)
        lst_all_ids = [request_id[0] for request_id in all_request_ids]

        test_ids = set(lst_all_ids) - set(lst_training_id)
        lst_test_ids = list(test_ids)

        return lst_test_ids


class NER:
    """
    Class to train NER model and to apply them on the testingSet for annotation inferrence
    """

    def __init__(self):
        pass

    @classmethod
    def get_training_testing_set(self):
        training_set = NER.get_training_set_paragraph(param["engine"])
        training_set = NER.stratified_sample(training_set)
        n = len(training_set)
        NB = n // 3
        testing_set = training_set[NB:-NB]
        training_set = [] + training_set[:NB] + training_set[-NB:]
        random.shuffle(training_set)

        return training_set, testing_set

    @classmethod
    # Train new NER model
    def train_new_NER(
        cls, TRAIN_DATA, model=None, output_dir="model", n_iter=100, drop_rate=0.5
    ):
        """
        Train a new NER model
        :param TRAIN_DATA: the training set
        :param model: the model if there is already one
        :param output_dir: the prefix of the name of the out put folder
        :param n_iter: the number of iterations
        :param drop_rate: the droprate
        """

        random.seed(0)

        if model is not None:
            nlp = spacy.load(model)  # load existing spaCy model
            print("Loaded model '%s'" % model)
        else:
            nlp = spacy.blank("fr")  # create blank Language class
            print("Created blank 'fr' model")

        # create the built-in pipeline components and add them to the pipeline
        # nlp.create_pipe works for built-ins that are registered with spaCy
        if "ner" not in nlp.pipe_names:
            ner = nlp.create_pipe("ner")
            nlp.add_pipe(ner, last=True)
        # otherwise, get it so we can add labels
        else:
            ner = nlp.get_pipe("ner")

        # add labels
        for _, annotations in TRAIN_DATA:
            for ent in annotations.get("entities"):
                ner.add_label(ent[2])

        # reset and initialize the weights randomly – but only if we're
        # training a new model
        optimizer = None
        if model is None:
            optimizer = nlp.begin_training()
        else:
            optimizer = nlp.resume_training()

        move_names = list(ner.move_names)

        # get names of other pipes to disable them during training
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

        with nlp.disable_pipes(
            *other_pipes
        ), warnings.catch_warnings():  # only train NER

            # show warnings for misaligned entity spans once
            warnings.filterwarnings("once", category=UserWarning, module="spacy")

            sizes = compounding(2.0, 10.0, 1.001)

            for itn in range(n_iter):
                print(f"Iteration N° {itn}:")
                random.shuffle(TRAIN_DATA)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(TRAIN_DATA, size=sizes)
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        sgd=optimizer,
                        drop=drop_rate,  # dropout - make it harder to memorise data
                        losses=losses,
                    )
                print("Losses", losses)

        # save model to output directory
        if output_dir is not None:
            output_dir = "../" + output_dir
            output_dir_ = Path(output_dir)
            if not output_dir_.exists():
                output_dir_.mkdir()

        model_dir = ""
        if model is None:
            model_dir = (
                output_dir
                + "/model_n_iter_"
                + str(n_iter)
                + "_droprate_"
                + str(drop_rate)
                + "_model_blanck"
            )
        else:
            model_dir = (
                output_dir
                + "/model_n_iter_"
                + str(n_iter)
                + "_droprate_"
                + str(drop_rate)
                + "_model_"
                + model
            )

        nlp.to_disk(model_dir)
        print("Saved model to", model_dir)

    @classmethod
    def test_ner(cls, dataset, model):
        """
        Apply the NER model on the trainingset and display the result in html format
        :param dataset: the dataset on wich we want to test the NER
        :param dataviz_dir: The visualisation folder
        :param model: the name of the model folder
        :param LIMIT: the limited number of request to treat
        """

        ner_model = spacy.load(model)
        lst_pred = []
        i = 0
        while i < len(dataset):
            text_i, ents_i = dataset[i]
            # prediction data
            doc_pred = ner_model(text_i)
            pred_data = {"text": text_i, "ents": [], "title": "predicted entities"}
            for ent in doc_pred.ents:
                if "fait" in ent.label_.lower():
                    continue
                pred_data["ents"].append(
                    {"start": ent.start_char, "end": ent.end_char, "label": ent.label_}
                )

            i += 1
            lst_pred.append(pred_data)

        return lst_pred

    @classmethod
    def test_ner_viz(
        cls, dataset, dataviz_dir="viz_annotations", model="model", LIMIT=20
    ):
        """
        Apply the NER model on the trainingset and display the result in html format
        :param dataset: the dataset on wich we want to test the NER
        :param dataviz_dir: The visualisation folder
        :param model: the name of the model folder
        :param LIMIT: the limited number of request to treat
        """

        html_dataviz_dir = os.path.join(dataviz_dir, model, "test")
        if not Path(html_dataviz_dir).exists():
            Path(html_dataviz_dir).mkdir(parents=True)

        ner_model = spacy.load(model)
        lst_pred = []
        i = 0
        while i < LIMIT and i < len(dataset):  # display only 20 documents
            text_i, ents_i = dataset[i]
            # original data
            original_data = {"text": text_i, "ents": [], "title": "original entities"}
            for ent in ents_i["entities"]:
                original_data["ents"].append(
                    {"start": ent[0], "end": ent[1], "label": ent[2]}
                )
            html_txt = displacy.render(
                [original_data], style="ent", jupyter=False, manual=True
            )
            html_path = os.path.join(
                html_dataviz_dir, "requete_" + str(i) + "_train_original_entities.html"
            )
            with open(html_path, "w") as file:
                file.write(html_txt)
            # prediction data
            doc_pred = ner_model(text_i)
            pred_data = {"text": text_i, "ents": [], "title": "predicted entities"}
            for ent in doc_pred.ents:
                if "fait" in ent.label_.lower():
                    continue
                pred_data["ents"].append(
                    {"start": ent.start_char, "end": ent.end_char, "label": ent.label_}
                )
            html_txt = displacy.render(
                [pred_data], style="ent", jupyter=False, manual=True
            )
            html_path = os.path.join(
                html_dataviz_dir,
                "requete_" + str(i) + "_train_prediction_entities.html",
            )
            with open(html_path, "w") as file:
                file.write(html_txt)
            i += 1
            lst_pred.append(pred_data)

        return lst_pred

    @classmethod
    def inferred_annotation(cls, dataset, lst_rq_ids, model="model"):
        """
        This function apply NER model on the testingset and saved the inferred annotation into the database
        :param dataset: the data on wich we want to test the NER model
        :param lst_rq_ids: the listt of requests id
        :param model: the model folder
        """

        ner_model = spacy.load(model)
        i = 0
        j = 0
        while i < len(dataset):  # display only 20 documents
            lst = dataset[i]
            while j < len(lst):
                text_j, ents_j = lst[j]

                # prediction data
                doc_pred = ner_model(text_j)
                for ent in doc_pred.ents:
                    if "fait" in ent.label_.lower():
                        continue

                    hash_object = hashlib.sha384(text_j.encode("utf-8"))
                    hex_dig = hash_object.hexdigest()

                    annotation = IAn(
                        ent.label_,
                        lst_rq_ids[i],
                        text_j[ent.start_char : (ent.end_char + 1)],
                        hex_dig,
                    )
                    annotation.save_to_db(param["session"])
                j = j + 1

            i = i + 1

    @classmethod
    def get_model_name(cls, model_dir, iter, droprate, model):
        return "../{}/model_n_iter_{}_droprate_{}_model_{}".format(
            model_dir, iter, droprate, model
        )

    @classmethod
    def idx_paragraph(cls, txt, sep):
        lst_paragraph = txt.split(sep)
        idx = 0
        n_sep = len(sep)
        lst_idx = []
        for p in lst_paragraph:
            n = len(p)
            lst_idx.append((idx, idx + n))
            idx = idx + n + n_sep

        return lst_idx

    @classmethod
    def is_in_paragraph(cls, p_start, p_end, a_start, a_end):
        assert p_start <= p_end
        assert a_start <= a_end

        return not (a_end < p_start or p_end < a_start)

    @classmethod
    def get_list_of_entities_per_paragraph(cls, lst_pargraph_idx, lst_entities):
        lst_result = []
        for pr_start, pr_end in lst_pargraph_idx:
            l = []
            for a_start, a_end, a_label in lst_entities:
                if cls.is_in_paragraph(pr_start, pr_end, a_start, a_end):
                    i_d = (a_start - pr_start) if a_start >= pr_start else 0
                    i_f = (a_end - pr_start) if a_end <= pr_end else (pr_end - pr_start)
                    l = l + [(i_d, i_f, a_label)]
            lst_result.append(l)
        return lst_result

    @classmethod
    def get_paragraph_training_set(cls, lst_paragraph_text, lst_entities_paragraph):
        tr_set = []
        for i in range(len(lst_paragraph_text)):
            txt = lst_paragraph_text[i]
            lst_entities = lst_entities_paragraph[i]
            tr_set.append((txt, {"entities": lst_entities}))

        return tr_set

    @classmethod
    def get_training_set_paragraph(cls, engine):
        """
        Connect to the database and get the trainingset
        :param engine: engine to execute database request
        :return: the NER training set
        """
        tr_set = []
        lst_request_id = Data.get_distinct_request_id(engine)
        for rq_id in lst_request_id:
            txt = Data.get_text_of_request(engine, rq_id)
            dct_entities = Data.get_dict_entities(engine, rq_id, txt)

            txt = txt.replace("###", "\n")
            lst_idx_paragraph = cls.idx_paragraph(txt, "\n\n")
            lst_txt_paragraph = txt.split("\n\n")
            lst_lst_entities = cls.get_list_of_entities_per_paragraph(
                lst_idx_paragraph, dct_entities["entities"]
            )
            l = cls.get_paragraph_training_set(lst_txt_paragraph, lst_lst_entities)
            tr_set = tr_set + l

        tr_set = Data.trim_entity_spans(tr_set)
        tr_set = Data.drop_overlapping_annotations(tr_set)

        return tr_set

    def get_training_chunck(cls, engine, rq_id):
        """
        Return the formated data for one request
        :param engine: engine to execute database request
        :param rq_id: request id
        :return: the formated training set for a request
        """
        text = cls.get_text_of_request(engine, rq_id)
        dct_entities = cls.get_dict_entities(engine, rq_id, text)
        text = text.replace("###", "\n")

        return text, dct_entities

    @classmethod
    def data_for_ner_evalutation(cls, model, dataset):

        testing_set = dataset

        df_result = pd.DataFrame(
            columns=["p_id", "A_moyen", "A_conclusion", "P_moyen", "P_conclusion"]
        )
        k = 0
        index = {}
        dct_p = {}
        for dset in testing_set:
            txt, dct = dset

            hash_object = hashlib.sha384(txt.encode("utf-8"))
            hex_dig = hash_object.hexdigest()

            dct_p["p_id"] = hex_dig
            dct_p["A_moyen"] = 0
            dct_p["A_conclusion"] = 0
            dct_p["P_moyen"] = 0
            dct_p["P_conclusion"] = 0
            index[hex_dig] = k

            for a_start, a_end, a_label in dct["entities"]:

                if a_label.lower() == "moyen":
                    dct_p["A_moyen"] = 1

                elif a_label.lower() == "conclusion":
                    dct_p["A_conclusion"] = 1

                df_result.loc[k] = [
                    dct_p["p_id"],
                    dct_p["A_moyen"],
                    dct_p["A_conclusion"],
                    dct_p["P_moyen"],
                    dct_p["P_conclusion"],
                ]
            k = k + 1

        pred_set = NER.test_ner(testing_set, model=model)

        for dset in pred_set:

            txt, lst_dct = dset["text"], dset["ents"]

            hash_object = hashlib.sha384(txt.encode("utf-8"))
            hex_dig = hash_object.hexdigest()
            idx = index[hex_dig]

            for aux in lst_dct:
                a_start, a_end, a_label = aux["start"], aux["end"], aux["label"]

                if a_label.lower() == "moyen":
                    df_result.loc[idx, "P_moyen"] = 1

                elif a_label.lower() == "conclusion":
                    df_result.loc[idx, "P_conclusion"] = 1

        df_result.to_excel("df_requete_for_metrics.xlsx")

        return df_result

    @classmethod
    def performance_criteria(cls, df, model_name, tst=True):
        print("\n")
        print("Data set : ")
        df_result = df.dropna()
        print(df_result)
        print("\n\n")
        print(
            """########################################   
    Criteres de qualite de l'annotation
############################################
                    """
        )

        dct_perf = {}

        num = sum(
            list((df_result.A_moyen == 1) & (df_result.A_moyen == df_result.P_moyen))
        )
        denom = sum(list(df_result.P_moyen))

        print(f"\n* Nombre paragraphe  : {len(df_result.P_conclusion)}")
        print(f"\n* Nombre paragraphe ayant le label moyen : {sum(df_result.A_moyen)}")
        print(
            f"\n* Nombre paragraphe ayant le label conclusion : {sum(df_result.A_conclusion)}"
        )
        print(f"\n* Nombre paragraphe prédit comme moyen : {sum(df_result.P_moyen)}")
        print(
            f"\n* Nombre paragraphe prédit comme conclusion : {sum(df_result.P_conclusion)}"
        )
        print(
            f"\n* Nombre de  paragraphe ayant le label moyen et predit comme tel {sum(list((df_result.A_moyen == 1) & (df_result.A_moyen == df_result.P_moyen)))}"
        )
        print(
            f"\n* Nombre de  paragraphe ayant le label conclusion et predit comme tel {sum(list((df_result.A_conclusion == 1) & (df_result.A_conclusion == df_result.P_conclusion)))}"
        )
        print("\n\n")

        dct_perf["model_name"] = model_name
        if denom == 0:
            dct_perf["precision_moyen"] = "NaN"
        else:
            dct_perf["precision_moyen"] = num / denom
        print(f"\n* Precision(moyen) == {dct_perf['precision_moyen']}")

        denom = sum(list(df_result.A_moyen))
        dct_perf["rappel_moyen"] = num / denom
        print(f"\n* Rappel(moyen) == {dct_perf['rappel_moyen']}")

        num = sum(
            list(
                (df_result.A_conclusion == 1)
                & (df_result.A_conclusion == df_result.P_conclusion)
            )
        )
        denom = sum(list(df_result.P_conclusion))

        if denom == 0:
            dct_perf["precision_conclusion"] = "NaN"
        else:
            dct_perf["precision_conclusion"] = num / denom
        print(f"\n* Precision(conclusion) == {dct_perf['precision_conclusion']}")

        denom = sum(list(df_result.A_conclusion))
        dct_perf["rappel_conclusion"] = num / denom
        print(f"\n* Rappel(conclusion) == {dct_perf['rappel_conclusion']}")

        ouput_dir = ""
        if tst:
            ouput_dir = "../model/" + model_name + "_testing_set_" + ".xlsx"
        else:
            ouput_dir = "../model/" + model_name + "_training_set_" + ".xlsx"
        df = pd.DataFrame(dct_perf, index=[0])
        df.to_excel(ouput_dir)

        return dct_perf

    @classmethod
    def stratified_sample(cls, tr_set):

        k = 0
        lst_v = []
        for ds in tr_set:
            if ds[1]["entities"] == []:
                lst_v.append(k)
            k = k + 1

        n = len(tr_set)
        lst_id_tr_set = list(range(n))
        lst_ent = list(set(lst_id_tr_set) - set(lst_v))

        n_ent = len(lst_ent)
        n_v = len(lst_v)

        l_r = []

        if n_ent > n_v:
            l_r = l_r + random.sample(lst_ent, n_v)
            l_r = l_r + lst_v
        else:
            l_r = l_r + random.sample(lst_v, n_ent)
            l_r = l_r + lst_ent

        return [tr_set[idx] for idx in l_r]


if __name__ == "__main__":
    pass
