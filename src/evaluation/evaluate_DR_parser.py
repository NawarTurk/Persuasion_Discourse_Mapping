
import os
import json
from utils.pt_dr_getters import get_DR_id_by_name
import warnings
from sklearn.metrics import f1_score, classification_report
from sklearn.exceptions import UndefinedMetricWarning



warnings.filterwarnings("ignore", category=UndefinedMetricWarning)

dataset_path = os.path.join("..", "dataset", "03_results", "dr_sample_prediction")

def evaluate_DR_parser_with_f1():
    pass


 
