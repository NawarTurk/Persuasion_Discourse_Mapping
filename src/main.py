
import os
from utils.data_preprocessing.extract_partially_annotated_dataset import extract_partially_annotated_dataset
from utils.data_preprocessing.populate_mock_DR import populate_mock_DR
from utils.data_preprocessing.load_dr_samples import load_dr_data_from_csv
from utils.populate_dr_predictions_for_dr_sample import populate_dr_predictions_for_dr_samples
from utils.llm_prompt_handlers.gpt_prompt_handler import get_gpt4_discourse_label
# from evaluation.evaluate_DR_parser import evaluate_DR_parser_with_f1

extract_partially_annotated_dataset()
# done

populate_mock_DR()
# done

load_dr_data_from_csv()
# done

populate_dr_predictions_for_dr_samples('prompt_2', get_gpt4_discourse_label)
# done



# evaluate_DR_parser_with_f1()
