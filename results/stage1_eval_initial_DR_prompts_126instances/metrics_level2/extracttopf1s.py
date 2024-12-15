import os
import json
script_dir = os.path.dirname(os.path.abspath(__file__))


dict = {}
for i in range (12, 34):
    dict[i] = {
        'macro': [],
        'parser': []
    }

macro_list = []
parsers = []
for file_name in os.listdir(script_dir):
    if file_name.endswith('.txt'):
        dir_path = os.path.join(script_dir, file_name)
        with open(dir_path, 'r') as f:
            line_num = 0
            for line in f:
                line_num +=1
                if line_num in range(12, 34):
                    try:
                        macro = float(line[-18:-10].strip())
                    except ValueError:  # Handle specific conversion error
                        print(f"Error processing line {line_num} in file {file_name}")
                        continue  # Skip this line and continue
                    except IndexError:  # Handle slicing error for short lines
                        print(f"Line {line_num} in file {file_name} is too short")
                        continue
                    parser = file_name[15:].split('_')[0] + '_' + file_name[15:].split('_')[1]
                    dict[line_num]['macro'].append(macro)
                    dict[line_num]['parser'].append(parser)
max_macros = []
parsers = []  
unique_parsers = set()     

for key, value in dict.items():
    max_macro = max(value['macro'])
    max_macro_index = value['macro'].index(max_macro)
    max_macros.append(max_macro)
    max_macro_parser = value['parser'][max_macro_index]
    parsers.append(max_macro_parser)
    unique_parsers.add(max_macro_parser)

                    
with open('result.json', 'w') as jsonfile:
    json.dump(dict, jsonfile, indent=2)

for i in unique_parsers:
    print(i)



# promptN01_gemini-1.5-pro
# promptN03_gemini-1.5-pro
# promptN02_claude-3-5-sonnet-20241022  <<<<<<<<<<<
# promptN09_gpt-4o
# promptN03_claude-3-5-sonnet-20241022
# promptN11_claude-3-5-sonnet-20241022
# promptN05_gpt-4o
# promptN10_claude-3-5-sonnet-20241022
# promptN02_gemini-1.5-pro  <<<<<<<<<<<<<<<<<<<<<<<<<<<<
# promptN03_gpt-4o
# promptN08_claude-3-5-sonnet-20241022
# promptN05_claude-3-5-sonnet-20241022  <<<<<<<<<<<<<<<<<<<<<<<<<<
# promptN11_gpt-4o
# promptN12_gpt-4o
# promptN05_gemini-1.5-pro
# promptN06_gemini-1.5-pro   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# promptN04_claude-3-5-sonnet-20241022



