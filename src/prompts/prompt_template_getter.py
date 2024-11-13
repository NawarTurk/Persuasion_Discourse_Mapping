
import sys

def get_prompt_template(prompt_key):
    try:
        with open(f'prompts/{prompt_key}.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        sys.exit(f'Prompt File was not found... {prompt_key}')




# PROMPT_TEMPLATES = {
#     "prompt_1": "Sev_Prompt",
#     "prompt_2": """Analyze the following paragraph and identify the most suitable PDTB Level 2 discourse relation label from this list:

# - Synchronous
# - Asynchronous
# - Cause
# - Cause+Belief
# - Cause+SpeechAct
# - Condition
# - Condition+SpeechAct
# - Negative-Condition
# - Negative-Condition+SpeechAct
# - Purpose
# - Concession
# - Concession+SpeechAct
# - Contrast
# - Similarity
# - Conjunction
# - Disjunction
# - Equivalence
# - Exception
# - Instantiation
# - Level-of-Detail
# - Manner
# - Substitution

# Paragraph:
# "{paragraph}"

# Provide only the label as your response, without any explanation (e.g., Synchronous, Cause+Belief, etc.).
# """,
#     "prompt_3": "GPT_Generated_Prompt meta-prompts",
#     "prompt_4": "Optional_additional_Sev_Prompt",
#     "prompt_5": "Optional_additional_Nawar_Prompt"
# }