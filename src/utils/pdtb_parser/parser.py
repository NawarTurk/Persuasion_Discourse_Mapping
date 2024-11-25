#fields
# 0  - Relation Type      - Explicit, Implicit, AltLex, AltLexC, Hypophora, EntRel, NoRel
# 1  - Conn SpanList      - SpanList of the Explicit Connective or the AltLex/AltLexC selection
# 2  - Conn Src           - Connective’s Source
# 3  - Conn Type          - Connective’s Type
# 4  - Conn Pol           - Connective’s Polarity
# 5  - Conn Det           - Connective’s Determinacy
# 6  - Conn Feat SpanList - Connective’s Feature SpanList
# 7  - Conn1              - Explicit Connective Head / First Implicit Connective
# 8  - SClass1A           - First Semantic Class of the First Connective
# 9  - SClass1B           - Second Semantic Class of the First Connective
# 10 - Conn2              - Second Implicit Connective
# 11 - SClass2A           - First Semantic Class of the Second Connective
# 12 - SClass2B           - Second Semantic Class of the Second Connective
# 13 - Sup1 SpanList      - SpanList of the First Argument’s Supplement
# 14 - Arg1 SpanList      - SpanList of the First Argument
# 15 - Arg1 Src           - First Argument’s Source
# 16 - Arg1 Type          - First Argument’s Type
# 17 - Arg1 Pol           - First Argument’s Polarity
# 18 - Arg1 Det           - First Argument’s Determinacy
# 19 - Arg1 Feat SpanList - SpanList of the First Argument’s Feature
# 20 - Arg2 SpanList      - SpanList of the Second Argument
# 21 - Arg2 Src           - Second Argument’s Source
# 22 - Arg2 Type          - Second Argument’s Type
# 23 - Arg2 Pol           - Second Argument’s Polarity
# 24 - Arg2 Det           - Second Argument’s Determinacy
# 25 - Arg2 Feat SpanList - SpanList of the Second Argument’s Feature
# 26 - Sup2 SpanList      - SpanList of the Second Argument’s Supplement
# 27 - Adju Reason        - The Adjudication Reason
# 28 - Adju Disagr        - The type of the Adjudication disagreement
# 29 - PB Role            - The PropBank role of the PropBank verb
# 30 - PB Verb            - The PropBank verb of the main clause of this relation
# 31 - Oﬀset              - The Conn SpanList of Explicit/AltLex/AltLexC tokens or the start point of the Arg2 of an Implicit/Hypophora/EntRel/NoRel tokens
# 32 - Provenance         - Indicates whether the token is a new PDTB3 token or has a corresponding PDTB2 token (see 8.2)
# 33 - Link               - The link id of the token


# "token_id": {
#     "token_id": "",
#     "text": "",
#     "actual_DR_level1": ",
#     "actual_DR_level2": "",
#     "predicted_DR_level2": null,
#     "test_token": "",
#     "actual_DR_level3": ""
#     "relation_type": ""
# }
import sys
import argparse
import os
import re
import json
from striprtf.striprtf import rtf_to_text

current_directory = os.getcwd()



def pdtb_preprocess_gold(gold_file_name, verbose_flag):
    dict_of_fields = []
    file_path = os.path.join(current_directory, gold_file_name)
    pattern = r'((EntRel|Explicit|Implicit|NoRel).*?(SAME\||CHANGED\|))'

    with open(file_path, 'r') as file:
        content = file.read()

    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        fields = match[0].split('|')
        dict_of_fields.append({
            "relation_type":fields[0],
            "conn_spanlist":fields[1],
            "conn_src":fields[2],
            "conn_type":fields[3],
            "conn_pol":fields[4],
            "conn_det":fields[5],
            "conn_feat_spanlist":fields[6],
            "conn1":fields[7],
            "s_class1a":fields[8],
            "s_class1b":fields[9],
            "conn2":fields[10],
            "s_class2a":fields[11],
            "s_class2b":fields[12],
            "sup1_spanlist":fields[13],
            "arg1_spanlist":fields[14],
            "arg1_src":fields[15],
            "arg1_type":fields[16],
            "arg1_pol":fields[17],
            "arg1_det":fields[18],
            "arg1_feat_spanlist":fields[19],
            "arg2_spanlist":fields[20],
            "arg2_src":fields[21],
            "arg2_type":fields[22],
            "arg2_pol":fields[23],
            "arg2_det":fields[24],
            "arg2_feat_spanlist":fields[25],
            "sup2_spanlist":fields[26],
            "adju_reason":fields[27],
            "adju_disagr":fields[28],
            "pb_role":fields[29],
            "pb_verb":fields[30],
            "offset":fields[31],
            "provenance":fields[32],
            "link":fields[33]
        })


    # Print each dictionary with a separator, taken from chatgpt
    if verbose_flag == 1:
        for i, entry in enumerate(dict_of_fields, start=1):
            print(f"Entry {i}:")
            for key, value in entry.items():
                print(f"  {key}: {value}")
            print("\n" + "-" * 50 + "\n")

    return dict_of_fields


def pdtb_preprocess_raw(raw_file_name, verbose_flag):

    dict_of_sentences = []
    file_path = os.path.join(current_directory, raw_file_name)
    pattern = r'(?<!\d)\.(?:\s|$)'

    with open(file_path, 'r') as file:
        content = file.read()

    content = rtf_to_text(content)

    content = content.replace(".START", "")

    clean_text = ' '.join(content.strip().split())

    sentences = re.split(pattern, clean_text)

    sentences = [sentence.strip() + '.' for sentence in sentences if sentence.strip()]

    dict_of_sentences = {i: sentence for i, sentence in enumerate(sentences)}

    # Print the enumerated dictionary
    if verbose_flag == 1:
        for idx, sentence in dict_of_sentences.items():
            print(f"{idx}: {sentence}")

    return dict_of_sentences


def pdtb_extract(fields, sentences, filename):

    sel_sentence = []
    write_list = []

    file_path = os.path.join(current_directory, filename)

    file_exists = 1 if os.path.exists(filename) == True else 0


    if file_exists == 1:

        with open(file_path, 'r') as file:
            old_list = json.load(file)

        token_ids = [int(entry["token_id"]) for entry in old_list if entry.get("token_id") and entry["token_id"].isdigit()]

        max_token_id = max(token_ids)
        print(max_token_id)


    if "max_token_id" in locals():
        start_id = max_token_id
    else:
        start_id = 0

    start_id+=1

    for i in range(len(fields)):
        if fields[i]["relation_type"] == "Explicit" or fields[i]["relation_type"] == "Implicit":
            relations = fields[i]["s_class1a"].split(".")
            relation_level1 = relations[0]
            relation_level2 = relations[1]

            relation_level3 = ""

            try:
                relation_level3 = relations[2]
            except:
                continue
            data = {
                "token_id": str(start_id),
                "text": str(sentences[i]),
                "actual_DR_level1": str(relation_level1),
                "actual_DR_level2": str(relation_level2),
                "predicted_DR_level2": None,
                "test_token": "y",
                "actual_DR_level3": str(relation_level3),
                "relation_type": str(fields[i]["relation_type"])
            }

            write_list.append(data)

            start_id+=1

    if file_exists == True:
        old_list.extend(write_list)


    if file_exists == True:
        with open('output.json', 'w') as file:
            json.dump(old_list, file, indent=4)
    else:
        with open(file_path, 'w') as file:
            json.dump(write_list, file, indent=4)


def main():

    print("start\n")
    parser = argparse.ArgumentParser(description="Input 2 file names: gold, raw and print verbose flag")

    parser.add_argument("file1", type=str, help="Gold file name")
    parser.add_argument("file2", type=str, help="Raw file name")
    parser.add_argument("file3", type=str, help="Output file name")
    parser.add_argument("verbose", type=str, help="enable print")

    args = parser.parse_args()

    file1 = args.file1
    file2 = args.file2
    file3 = args.file3
    verbose_flag = args.verbose

    dict_of_fields    = pdtb_preprocess_gold(file1, verbose_flag)
    dict_of_sentences = pdtb_preprocess_raw(file2, verbose_flag)
    # print(dict_of_sentences[0])
    # print(dict_of_fields[0])
    pdtb_extract(dict_of_fields, dict_of_sentences, file3)

if __name__ == "__main__":
    main()
