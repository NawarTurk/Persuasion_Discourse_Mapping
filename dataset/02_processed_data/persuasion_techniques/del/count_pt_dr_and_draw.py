import json

with open('PT_dataset_A.json', 'r',encoding='utf-8') as f:
    data= json.load(f)

    


for key, value in data.items():
    data[key]['predicted_DR']=''
    data[key]['parser']=''
    data[key]['DR']=''



with open('PT_dataset_A_decreased.json', 'w', encoding='utf-8') as f2:
    json.dump(data, f2, indent=2, ensure_ascii=False )