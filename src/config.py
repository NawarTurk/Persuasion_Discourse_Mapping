
# API keys
OPENAI_API_KEY = ""
GEMINI_API_KEY = ""
CLAUDE_API_KEY = ""
# Prompt 
PROMPT_KEY = 'promptN10'  

#Delay
PROCESSING_DELAY_SECONDS = 3 # seconds

# Parser
PARSER_ID = 2# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#  1 for the gpt_prompt_handler
#  2 for the gemini_prompt_handler   
#  3 for the claude_prompt_handler   

# NOTE: For the following Chain of Thoughts prompts, it ignores PROMPT_KEY as the prompts are hardcoded inside the functions for now
#  10 for multi_level_gpt_prompt_handler_v2  
#  12 for multi_level_gemini_prompt_handler_v2  
#  14 for multi_level_claude_prompt_handler_v2  

# Model names
OPENAI_MODEL_NAME = "gpt-4o" 

# GEMINI_MODEL_NAME = 'gemini-2.0-flash-exp'
# GEMINI_MODEL_NAME = "gemini-1.5-pro"  
# GEMINI_MODEL_NAME = 'tunedModels/finetuningdatasetpromptn01-efbmd6jctg4a'  # promptN01
# GEMINI_MODEL_NAME = 'tunedModels/finetuningdatasetpromptn02-62qcosqvlxl3'  # promptN02
# GEMINI_MODEL_NAME = 'tunedModels/finetuningdatasetpromptn03-au96dwywgw6y'  # promptN03
# GEMINI_MODEL_NAME = 'tunedModels/finetuningdatasetpromptn04-nvqkj0rndavp'  # promptN04
# GEMINI_MODEL_NAME = "tunedModels/finetuningdatasetpromptn05-vqaiqxi25ly0"  # promptN05
# GEMINI_MODEL_NAME = 'tunedModels/finetuningdatasetpromptn06-n20cevrii99m'  # promptN06
# GEMINI_MODEL_NAME = 'tunedModels/finetuningdatasetpromptn07-74qpv7itz4ha'
# GEMINI_MODEL_NAME = 'tunedModels/finetuningdatasetpromptn08-zodll2yby8mp'
# GEMINI_MODEL_NAME = 'tunedModels/finetuningdatasetpromptn09-jksytsz7eg5v'
GEMINI_MODEL_NAME = 'tunedModels/finetuningdatasetpromptn10-fgouvknl4rp5'


CLAUDE_MODEL_NAME = "claude-3-5-sonnet-20241022"


### PT DATA SET PARSING FOR DR ###
PT_DATASET = 'PT_dataset_2'  # Name of the dataset containing persuasion techniques (PTs)
BATCH_SIZE = 20  # Number of parses to perform before saving the results
API_CALL_DELAY_SEC = 10  # Delay in seconds between each API call
RUN_DELAY_SEC = 50  # Delay in seconds after saving results (before the next batch)



