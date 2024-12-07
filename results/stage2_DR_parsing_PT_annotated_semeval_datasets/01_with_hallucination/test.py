import json

with open('semeval_PT_dataset_1_claude-3-5-sonnet-20241022_promptN05.json', 'r', encoding='utf-8') as jsonfile:
    data1 = json.load(jsonfile)

with open('semeval_PT_dataset_2_claude-3-5-sonnet-20241022_promptN05.json', 'r', encoding='utf-8') as jsonfile:
    data2 = json.load(jsonfile)

data = {**data1, **data2}


for key, value in data.items():
    value['predicted_DR'] = value['DR']
    value['parser'] = 'gemini-1.5-pro_promptN06'
    dr = value.pop('DR')
    value['DR'] = dr

with open('combined_1_and_2_semeval_PT_dataset_claude-3-5-sonnet-20241022_promptN05.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent= 2, ensure_ascii=False)

print(len(data1))
print(len(data2))
print(len(data))


level2_to_level1 = {
        # Temporal
        "synchronous": "temporal",
        "asynchronous": "temporal",

        # Contingency
        "cause": "contingency",
        "cause+belief": "contingency",
        "cause+speechact": "contingency",
        "condition": "contingency",
        "condition+speechact": "contingency",
        "negative-condition": "contingency",
        "negative-condition+speechact": "contingency",
        "purpose": "contingency",

        # Comparison
        "concession": "comparison",
        "concession+speechact": "comparison",
        "contrast": "comparison",
        "similarity": "comparison",

        # Expansion
        "conjunction": "expansion",
        "disjunction": "expansion",
        "equivalence": "expansion",
        "exception": "expansion",
        "instantiation": "expansion",
        "level-of-detail": "expansion",
        "manner": "expansion",
        "substitution": "expansion"
    }


with open('combined_1_and_2_semeval_PT_dataset_gemini-1.5-pro_promptN06.json', 'r') as jsonfile:
    data = json.load(jsonfile)

for key, value in data.items():
    if value['DR'] not in level2_to_level1:
        print(key)
        print(value['DR'])