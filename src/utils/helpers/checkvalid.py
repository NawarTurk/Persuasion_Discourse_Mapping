import json

DR_level2 = {
        "synchronous", "asynchronous", "cause", "cause+belief", "cause+speechact", "condition", "condition+speechact", "negative-condition", 
        "negative-condition+speechact", "purpose", "concession", "concession+speechact", "contrast", "similarity", "conjunction", "disjunction", 
        "equivalence", "exception", "instantiation", "level-of-detail", "manner", "substitution"}

with open('../../../results/stage2_DR_parsing_PT_annotated_semeval_datasets/01_with_hallucination/PT_dataset_1_gemini-1.5-pro_promptN02.json', 'r', encoding='utf-8') as jsonfile:
    data = json.load(jsonfile)

for key, value in data.items():
    if value['DR'] not in DR_level2:
        print(f'{value['DR']} ____ {key}')
