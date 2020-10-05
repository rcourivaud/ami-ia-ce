from ner import *
import argparse
from base import logging_utils as log

#######################
# Default values
# model_name : model name eg: model_n_iter_9_droprate_0.5_model_blanck
#######################
model_name = ""

ner_infer_annotations_logger = log.get_logger(__name__, "ner_infer_annotations")

class TestNer:
    def __init__(self):
        pass

    @classmethod
    def test_ner(cls, model_name):
        ner_infer_annotations_logger.info("Calling test_ner(cls, model_name)")
        lst_tst_set, lst_ids = Data.get_testing_set(param["engine"])
        NER.inferred_annotation(lst_tst_set, lst_ids, model_name)
        ner_infer_annotations_logger.info("Done with test_ner(cls, model_name)")


if __name__ == "__main__":
    # Initiate the parser
    parser = argparse.ArgumentParser()

    # Add long and short argument
    parser.add_argument("--model_name", "-mn", help="set the model name")

    # Read arguments from the command line
    args = parser.parse_args()

    if args.model_name:
        model_name = args.model_name

    MODEL = os.path.join(os.path.dirname(__file__), "../model/{}".format(model_name))

    # Check for --width
    if args.model_name:
        TestNer.test_ner(MODEL)
