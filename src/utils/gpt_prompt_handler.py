import openai

'''
Name: openai
Version: 0.28.0


models = openai.Model.list()
print([model['id'] for model in models['data']])

# would result in ...
['tts-1', 'tts-1-1106', 'gpt-4-turbo-2024-04-09', 'gpt-4o', 'gpt-4o-2024-08-06', 'dall-e-2', 'whisper-1', 'gpt-3.5-turbo-instruct', 'tts-1-hd-1106', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'babbage-002', 'gpt-4o-2024-05-13', 'davinci-002', 'dall-e-3', 'gpt-4o-realtime-preview', 'gpt-4o-realtime-preview-2024-10-01', 'tts-1-hd', 'chatgpt-4o-latest', 'gpt-4-turbo-preview', 'gpt-4-1106-preview', 'text-embedding-ada-002', 'gpt-3.5-turbo-16k', 'gpt-4-turbo', 'text-embedding-3-small', 'text-embedding-3-large', 'gpt-4o-mini-2024-07-18', 'gpt-3.5-turbo-1106', 'gpt-4o-mini', 'gpt-4o-audio-preview', 'gpt-4o-audio-preview-2024-10-01', 'gpt-4-0613', 'gpt-4-0125-preview', 'gpt-4', 'gpt-3.5-turbo-instruct-0914']

'''

key = "..."

openai.api_key = key

def get_discourse_relation(paragraph, prompt_template):
    prompt = prompt_template.format(paragraph=paragraph)

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response['choices'][0]['message']['content'].strip()

    return result


### TEST ###
prompt_template = """Analyze the following paragraph and identify its primary discourse relation.
Choose the most relevant relation from this list:
- Temporal: Indicates a time sequence (e.g., "then," "after").
- Contingency: Shows causation or conditions (e.g., "because," "if").
- Comparison: Highlights contrast or similarity (e.g., "however," "but").
- Expansion: Adds additional, related information (e.g., "and," "also").

Paragraph:
"{paragraph}"

Provide the discourse relation as a single label: Temporal, Contingency, Comparison, or Expansion.
"""

paragraph = "The company announced record profits this quarter; however, the CEO warned that economic uncertainty could impact future growth."

print(get_discourse_relation(paragraph, prompt_template))