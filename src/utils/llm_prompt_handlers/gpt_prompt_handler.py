import openai
import config
'''
Name: openai
Version: 0.28.0

models = openai.Model.list()
print([model['id'] for model in models['data']])

# would result in ...
['tts-1', 'tts-1-1106', 'gpt-4-turbo-2024-04-09', 'gpt-4o', 'gpt-4o-2024-08-06', 'dall-e-2', 'whisper-1', 'gpt-3.5-turbo-instruct', 'tts-1-hd-1106', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'babbage-002', 'gpt-4o-2024-05-13', 'davinci-002', 'dall-e-3', 'gpt-4o-realtime-preview', 'gpt-4o-realtime-preview-2024-10-01', 'tts-1-hd', 'chatgpt-4o-latest', 'gpt-4-turbo-preview', 'gpt-4-1106-preview', 'text-embedding-ada-002', 'gpt-3.5-turbo-16k', 'gpt-4-turbo', 'text-embedding-3-small', 'text-embedding-3-large', 'gpt-4o-mini-2024-07-18', 'gpt-3.5-turbo-1106', 'gpt-4o-mini', 'gpt-4o-audio-preview', 'gpt-4o-audio-preview-2024-10-01', 'gpt-4-0613', 'gpt-4-0125-preview', 'gpt-4', 'gpt-3.5-turbo-instruct-0914']

'''

openai.api_key = config.OPENAI_API_KEY
model_name = config.OPENAI_MODEL_NAME


def gpt_prompt_handler(paragraph, prompt_template):
    prompt = prompt_template.format(paragraph=paragraph)

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response['choices'][0]['message']['content'].strip()

    return result
