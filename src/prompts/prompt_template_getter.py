import sys
import os

def get_prompt_template(prompt_key):
    try:
        path = os.path.join('prompts', f'{prompt_key}.txt')
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        sys.exit(f'Prompt File was not found... {prompt_key}')
