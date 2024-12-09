import os
import json
import glob
import pandas as pd

def get_data_from_file(input_file):
    file_path = f"../../dataset/mock_data/{input_file}" #complete_dataset_with_mock_DR.json
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_data_from_files(file_path):

    data_list = []
    # file_path = f"../../dataset/mock_data"
    os.chdir(file_path)

    for file in glob.glob("*.json"):
        with open(file, 'r') as f:
            data_list.append(json.load(f))
    return data_list

def extract_data_frequencies(data):
    dr_freq_dict = {}
    pt_freq_dict = {}
    cooccurrence_freq_dict = {}

    for key, item in data.items():
        dr = item["DR"]
        pt = item["PT"]

        dr_freq_dict[dr] = dr_freq_dict[dr] + 1 if dr in dr_freq_dict else 1
        pt_freq_dict[pt] = pt_freq_dict[pt] + 1 if pt in pt_freq_dict else 1
        cooccurrence_freq_dict[(dr, pt)] = cooccurrence_freq_dict[(dr, pt)] + 1 if (dr, pt) in cooccurrence_freq_dict else 1

    # print(dr_freq_dict)

    return dr_freq_dict, pt_freq_dict, cooccurrence_freq_dict

