
import os
import argparse
from utils.data_preprocessing.extract_partially_annotated_dataset import extract_partially_annotated_dataset
from utils.data_preprocessing.populate_mock_DR import populate_mock_DR
from utils.data_preprocessing.load_dr_samples import load_dr_data_from_csv
from utils.populate_dr_predictions import populate_dr_predictions
from evaluation.evaluate_DR_parser import evaluate_DR_parser_with_f1
from evaluation.evaluate_DR_parser_lvl1 import evaluate_DR_parser_with_f1_lvl1

parser = argparse.ArgumentParser(description='Run parts of the script based on flags provided.')
parser.add_argument('--preprocess', action='store_true', help='Run data preprocessing')
parser.add_argument('--parseDR', action='store_true', help='Run DR parsing')
parser.add_argument('--evaluate', action='store_true', help='Run evaluation')
args = parser.parse_args()

if args.preprocess:  # Below is already done for you!
    extract_partially_annotated_dataset()  # from semeval PT dataset
    populate_mock_DR()  # resutls in dataset with actual PT and fake DR for testing statistical code
    load_dr_data_from_csv()  # to generate PDTB DR sample for testing prompts

if args.parseDR:
    populate_dr_predictions()

if args.evaluate:
    evaluate_DR_parser_with_f1()
    evaluate_DR_parser_with_f1_lvl1()



