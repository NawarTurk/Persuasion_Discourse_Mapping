
import os
import argparse
from utils.data_preprocessing.extract_semeval_PT_data import extract_semeval_PT_data
from utils.data_preprocessing.generate_mock_DR_into_semeval_data import generate_mock_DR_into_semeval_data
from utils.data_preprocessing.extract_sample1_DR_data import extract_sample1_DR_data
from utils.data_preprocessing.extract_semeval_PT_multiple_datasets import extract_semeval_PT_multiple_datasets

from DR_parsers.DR_parser_with_LLM import parser_DR_with_LLM
from evaluation.evaluate_DR_parser_lvl2 import evaluate_DR_parser_with_f1
from evaluation.evaluate_DR_parser_lvl1 import evaluate_DR_parser_with_f1_lvl1

parser = argparse.ArgumentParser(description='Run parts of the script based on flags provided.')
parser.add_argument('--preprocess', action='store_true', help='Run data preprocessing')
parser.add_argument('--parseDR', action='store_true', help='Run DR parsing')
parser.add_argument('--evaluate', action='store_true', help='Run evaluation')
args = parser.parse_args()

if args.preprocess:  # Below is already done for you!
    extract_semeval_PT_data()  # from semeval PT dataset
    generate_mock_DR_into_semeval_data()  # resutls in dataset with actual PT and fake DR for testing statistical code
    extract_semeval_PT_multiple_datasets()
    extract_sample1_DR_data()  # to generate PDTB DR sample for testing prompts

if args.parseDR:
    parser_DR_with_LLM()

if args.evaluate:
    evaluate_DR_parser_with_f1()
    evaluate_DR_parser_with_f1_lvl1()



