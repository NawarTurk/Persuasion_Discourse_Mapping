import json 

with open('PT_dataset_A_gemini-2.0-flash-exp_promptN05.json', 'r') as f:
    data= json.load(f)
    print(len(data))
count_dict = {}
for key, value in data.items():
    if value['PT'] not in count_dict:
        count_dict[value['PT']] = 1
    count_dict[value['PT']] += 1

count_dict = dict(sorted(count_dict.items(), key=lambda item: item[1], reverse=True))
print(json.dumps(count_dict, indent=2))

    

# import json
# DR_level2 = {
#         "synchronous", "asynchronous", "cause", "cause+belief", "cause+speechact", "condition", "condition+speechact", "negative-condition", 
#         "negative-condition+speechact", "purpose", "concession", "concession+speechact", "contrast", "similarity", "conjunction", "disjunction", 
#         "equivalence", "exception", "instantiation", "level-of-detail", "manner", "substitution"}

# counter = 0
# for key, value in data.items():
#     if value['DR'] not in DR_level2:
#         print(f'{value['DR']} __{value['predicted_DR']}__ {key}')
#         counter += 1
#         # print(f'{value['DR']} ___ {key}')

# print(counter)


# #######

# # with open('PT_dataset_1_gemini-2.0-flash-exp_promptN05.json', 'r', encoding='utf-8') as f:
# #     data1 = json.load(f)
# # with open('PT_dataset_2_gemini-2.0-flash-exp_promptN05.json', 'r', encoding ='utf-8') as f:
# #     data2 = json.load(f)
# # data = {**data1, **data2}
# # print(len(data1))
# # print(len(data2))
# # print(len(data))
# # with open('PT_dataset_A_gemini-2.0-flash-exp_promptN05.json', 'w', encoding = 'utf-8') as jsonfile:
# #     json.dump(data, jsonfile, indent=2, ensure_ascii=False)


