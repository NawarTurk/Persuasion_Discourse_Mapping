import google.generativeai as genai
import sys
sys.path.append('../../') 
import config

api_key = config.GEMINI_API_KEY
model_name = config.GEMINI_MODEL_NAME

model_name = 'tunedModels/finetuningdataset-58qgwpre8qt6'
genai.configure(api_key=api_key)

for model_info in genai.list_tuned_models():
    print(model_info.name)

model = genai.GenerativeModel(model_name)
response = model.generate_content('I did not eat breakfast, therefore, i am hungry')

print((response.text).strip())