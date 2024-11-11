
import os
from utils.data_preprocessing.extract_partially_annotated_dataset import extract_partially_annotated_dataset
from utils.data_preprocessing.populate_mock_DR import populate_mock_DR
from utils.data_preprocessing.load_dr_samples import load_dr_data_from_csv
from utils.populate_dr_predictions import populate_dr_predictions
from evaluation.evaluate_DR_parser import evaluate_DR_parser_with_f1


### PREPROCESSING ###
# Below is already done for you!
# extract_partially_annotated_dataset()
# populate_mock_DR()
# load_dr_data_from_csv()


### DR PARSING ###
# Change values in config.py and run main
# populate_dr_predictions()

### F1 Evaluation ###
# run this after you are do the de
# evaluate_DR_parser_with_f1()


