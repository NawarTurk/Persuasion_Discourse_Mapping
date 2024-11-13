
# API keys
OPENAI_API_KEY = "key"
GEMINI_API_KEY = "key"
CLAUDE_API_KEY = "your_claude_api_key_here"

# Model names
OPENAI_MODEL_NAME = "gpt-4-turbo"
# ['tts-1', 'tts-1-1106', 'gpt-4-turbo-2024-04-09', 'gpt-4o', 'gpt-4o-2024-08-06', 'dall-e-2', 'whisper-1', 'gpt-3.5-turbo-instruct', 'tts-1-hd-1106', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0125', 'babbage-002', 'gpt-4o-2024-05-13', 'davinci-002', 'dall-e-3', 'gpt-4o-realtime-preview', 'gpt-4o-realtime-preview-2024-10-01', 'tts-1-hd', 'chatgpt-4o-latest', 'gpt-4-turbo-preview', 'gpt-4-1106-preview', 'text-embedding-ada-002', 'gpt-3.5-turbo-16k', 'gpt-4-turbo', 'text-embedding-3-small', 'text-embedding-3-large', 'gpt-4o-mini-2024-07-18', 'gpt-3.5-turbo-1106', 'gpt-4o-mini', 'gpt-4o-audio-preview', 'gpt-4o-audio-preview-2024-10-01', 'gpt-4-0613', 'gpt-4-0125-preview', 'gpt-4', 'gpt-3.5-turbo-instruct-0914']

GEMINI_MODEL_NAME = "gemini-1.5-flash"
# +-------------------------+-----------------------------------------------------------+
# | Model Variant           | Optimized for                                             |
# +-------------------------+-----------------------------------------------------------+
# | Gemini 1.5 Flash        | Fast and versatile performance across a variety of tasks |
# +-------------------------+-----------------------------------------------------------+
# | Gemini 1.5 Flash-8B     | High volume and lower intelligence tasks                  |
# +-------------------------+-----------------------------------------------------------+
# | Gemini 1.5 Pro          | Complex reasoning tasks requiring more intelligence       |
# +-------------------------+-----------------------------------------------------------+
# | Gemini 1.0 Pro          | Natural language tasks, multi-turn text and code chat,   |
# |                         | and code generation                                       |
# +-------------------------+-----------------------------------------------------------+
# | Text Embedding          | Measuring the relatedness of text strings                 |
# +-------------------------+-----------------------------------------------------------+
# | AQA                     | Providing source-grounded answers to questions            |
# +-------------------------+-----------------------------------------------------------+
# source: https://ai.google.dev/gemini-api/docs/models/gemini

CLAUDE_MODEL_NAME = "CLAUDE model name here"

# Prompt 
PROMPT_KEY = 'prompt_2'

# Parser
PARSER_ID = 1
#  1 for the gpt_prompt_handler
#  2 for the gemini_prompt_handler   
#  3 for the claude_prompt_handler   NOT DONE YET

#Delay
PROCESSING_DELAY_SECONDS = 7