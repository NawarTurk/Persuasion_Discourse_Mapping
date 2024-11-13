import google.generativeai as genai
import config

api_key = config.GEMINI_API_KEY
model_name = config.GEMINI_MODEL_NAME

genai.configure(api_key=api_key)

def gemini_prompt_handler(paragraph, prompt_template):
    prompt = prompt_template.format(paragraph=paragraph)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return (response.text)
