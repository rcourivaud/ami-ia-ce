from ner import *
import argparse
from base import logging_utils as log

#######################
# Default values
# m : model name eg: None, fr_core_news_md
# ouput_dir : the directory where to store the model
# it : the number of iterations
# dr : drop rate to consider
#######################
m, output_dir, it, dr = None, "model", "5", "0.2"

ner_train_model_logger = log.get_logger(__name__, "ner_train_model")

class TrainNer:
    def __init__(self):
        pass

    @classmethod
    def train_ner_model(cls, m, ouput_dir, it, dr):
        ner_train_model_logger.info("Calling train_ner_model(cls, m, ouput_dir, it, dr)")
        tr_set, tst_set = NER.get_training_testing_set()

        NER.train_new_NER(tr_set, m, ouput_dir, it, dr)
        s = m
        if m is None:
            s = "blanck"

        model_name = NER.get_model_name("model", it, dr, s)

        print("\n\nPerformance on the testing_set\n")
        df = NER.data_for_ner_evalutation(model_name, tst_set)
        NER.performance_criteria(df, model_name)

        print("\n\nPerformance on the training_set\n")
        df = NER.data_for_ner_evalutation(model_name, tr_set)
        _ = NER.performance_criteria(df, model_name, False)
        ner_train_model_logger.info("Done with train_ner_model(cls, m, ouput_dir, it, dr)")


if __name__ == "__main__":
    # Initiate the parser
    parser = argparse.ArgumentParser()

    # Add long and short argument
    parser.add_argument("--iteration", "-it", help="set output number  of iterations")
    parser.add_argument("--drop_rate", "-dr", help="set output the drop rate")
    parser.add_argument("--output_dir", "-o", help="set output directory")
    parser.add_argument("--model", "-m", help="set model to update")

    # Read arguments from the command line
    args = parser.parse_args()

    # Check for --width
    if args.iteration:
        it = int(args.iteration)
    if args.drop_rate:
        dr = float(args.drop_rate)
    if args.output_dir:
        output_dir = args.output_dir
    if args.model:
        m = args.model

    TrainNer.train_ner_model(m, output_dir, it, dr)
