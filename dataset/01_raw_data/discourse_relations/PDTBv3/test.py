import os
import json

# Get the absolute path to the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
outputpath = os.path.join(script_dir, 'output')
# Construct the path to the 'gold' directory
gold_dir = os.path.join(script_dir, 'gold')

PDTBv3_dict = {}

# Iterate through each subdirectory in 'gold'
for subdir in os.listdir(gold_dir):
    subdir_path = os.path.join(gold_dir, subdir)

    # Check if the current path is a directory
    if os.path.isdir(subdir_path):
  
        files = os.listdir(subdir_path)
        files.sort()  # Sorts the list of filenames alphabetically

        # Print the sorted filenames
        for wsj_file in files:
            wsj_gold_file_path = os.path.join(subdir_path, wsj_file)
            gold_line_numb = 1

            with open(wsj_gold_file_path, 'r') as gold_file:
                for line in gold_file:
                    fields = line.strip().split('|')


                    relation_type = fields[0]
                    DR_relations = fields[8]
                    DR_levels = DR_relations.split('.')
                    DR_level1 = DR_levels[0] if DR_levels else ''
                    DR_level2 = DR_levels[1] if len(DR_levels) > 1 else ''
                    DR_level3 = DR_levels[2] if len(DR_levels) > 2 else ''
                    SpanList_1st_arg = fields[14]
                    SpanList_2nd_arg = fields[20]

                    PDTBv3_dict[f'{subdir}.{wsj_file}.{gold_line_numb}'] = {
                        'folder': subdir,
                        'file': wsj_file,
                        'gold_line_number': gold_line_numb,
                        'relation_type': relation_type,
                        'DR_relations': DR_relations,
                        'DR_level1': DR_level1,
                        'DR_level2': DR_level2,
                        'DR_level3': DR_level3,
                        'spanList_1st_arg': SpanList_1st_arg,
                        'spanList_2nd_arg': SpanList_2nd_arg,
                        'first_arg': '',
                        'second_arg': '',
                        'paragaph': '',
                        'DR_level1_prediction': '',
                        'DR_level2_prediction': '',
                        'DR_level3_prediction': '',
                    }

                    gold_line_numb += 1          
                     

for key, instance in PDTBv3_dict.items():
    if ';' not in instance['spanList_1st_arg'] and ';' not in instance['spanList_2nd_arg']:
        raw_path = os.path.join(script_dir, 'raw', instance['folder'], instance['file'])

        start1, end1 = map(int, instance['spanList_1st_arg'].split('..'))
        start2, end2 = map(int, instance['spanList_2nd_arg'].split('..'))

        with open(raw_path, 'r') as raw_file:
            raw_text = raw_file.read()
            first_arg = raw_text[start1:end1].strip()
            second_arg = raw_text[start2:end2].strip()

            instance['first_arg'] = first_arg
            instance['second_arg'] = second_arg


with open(outputpath, 'w') as jsonfile:
    json.dump(PDTBv3_dict, jsonfile, indent=2)






# with open(raw_path, 'r') as raw_file:
#     raw_text = raw_file.read()

#     try:
#         start1, end1 = map(int, SpanList_1st_arg.split('..'))
#         start2, end2 = map(int, SpanList_2nd_arg.split('..'))

#         first_arg = raw_text[start1:end1].strip()
#         second_arg = raw_text[start2:end2].strip()
#     except:
#         first_arg = ''
#         second_arg = ''

#     PDTBv3_dict[f'{subdir}.{wsj_file}.{gold_line_numb}']['first_arg'] = first_arg
#     PDTBv3_dict[f'{subdir}.{wsj_file}.{gold_line_numb}']['second_arg'] = second_arg