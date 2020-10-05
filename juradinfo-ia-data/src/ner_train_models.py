from ner import *
import pandas as pd
import os
import argparse
from base import logging_utils as log
import time

#######################
# Default values
# itx : the maximun number of iterations to considered
#######################
itx = 20

ner_train_models_logger = log.get_logger(__name__, "ner_train_models")

class TrainNer:
    def __init__(self):
        pass

    # get the list of xlsx files
    @classmethod
    def get_files(cls, ext, input_dir):
        """ :returns the list of all pdf files containt in a folder and its subfolders
            :param input_dir: folder that containt pdffiles"""
        ner_train_models_logger.info("Calling get_files(cls, ext, input_dir)")
        return [
            os.path.join(root, name)
            for root, dirs, files in os.walk(input_dir)
            for name in files
            if name.endswith(ext)
        ]
        ner_train_models_logger.info("Done with  get_files(cls, ext, input_dir)")

    @classmethod
    def merge_results(cls):
        """
        Merge the xlsx file containning performances of NER models
        """
        ner_train_models_logger.info("Calling merge_results(cls)")
        # get the data from the file
        lst_xlsx = cls.get_files(".xlsx", "../../model")

        lst_md_name = []

        lst_precision_moyen = []
        lst_rappel_moyen = []

        lst_precision_conclusion = []
        lst_rappel_conclusion = []

        lst_n_iter = []
        lst_drop_rate = []
        lst_transfert = []

        for f in lst_xlsx:
            df = pd.read_excel(f)
            model_name = df.iloc[0, 1]
            l_aux = model_name.split("_")
            lst_n_iter.append(l_aux[3])
            lst_drop_rate.append(l_aux[5])
            lst_transfert.append("_".join(l_aux[7:]))

            lst_md_name.append(df.iloc[0, 1])

            lst_precision_moyen.append(df.iloc[0, 2])
            lst_rappel_moyen.append(df.iloc[0, 3])

            lst_precision_conclusion.append(df.iloc[0, 4])
            lst_rappel_conclusion.append(df.iloc[0, 5])

        # merge the data to the result dictionnary
        dct = {}
        dct["model_name"] = lst_md_name
        dct["nb_iter"] = lst_n_iter
        dct["drop_rate"] = lst_drop_rate
        dct["Transfert Learning"] = lst_transfert
        dct["precision_moyen"] = lst_precision_moyen
        dct["rappel_moyen"] = lst_rappel_moyen
        dct["precision_conclusion"] = lst_precision_conclusion
        dct["rappel_conclusion"] = lst_rappel_conclusion

        # save the result dictionnary as xlsx file
        df = pd.DataFrame(dct)
        df.to_excel("result.xlsx")
        ner_train_models_logger.info("Done with merge_results(cls)")

    @classmethod
    def train_ner_models(cls, itx):
        ner_train_models_logger.info("Calling train_ner_models(cls, itx)")
        start_time = time.time()
        tr_set, tst_set = NER.get_training_testing_set()

        lst_model = [None, "fr_core_news_md"]
        for it in range(2, itx, 1):
            for dr in [0.2, 0.25, 0.3, 0.35, 0.5]:
                for m in lst_model:
                    NER.train_new_NER(tr_set, m, "model", it, dr)
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

        cls.merge_results()
        elapsed_time = time.time() - start_time
        ner_train_models_logger.info(f"Done with train_ner_models(cls, itx), duration of the execution : {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}")


if __name__ == "__main__":
    # Initiate the parser
    parser = argparse.ArgumentParser()

    # Add long and short argument
    parser.add_argument(
        "--iteration_max", "-itx", help="set output number max of iterations"
    )

    # Read arguments from the command line
    args = parser.parse_args()

    # Check for --width
    if args.iteration_max:
        itx = int(args.iteration_max)
        TrainNer.train_ner_models(itx)
    else:
        TrainNer.train_ner_models()
