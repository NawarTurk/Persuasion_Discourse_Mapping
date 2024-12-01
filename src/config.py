
# API keys
OPENAI_API_KEY = ""
GEMINI_API_KEY = "-"
CLAUDE_API_KEY = ""
# Prompt 
PROMPT_KEY = 'promptN01'

#Delay
PROCESSING_DELAY_SECONDS = 9  # seconds

# Parser
PARSER_ID = 2 # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#  1 for the gpt_prompt_handler
#  2 for the gemini_prompt_handler   
#  3 for the claude_prompt_handler   

# NOTE: For the following Chain of Thoughts prompts, it ignores PROMPT_KEY as the prompts are hardcoded inside the functions for now
#  9 for multi_level_gpt_prompt_handler_v1  
#  10 for multi_level_gpt_prompt_handler_v2  
#  11 for multi_level_gemini_prompt_handler_v1  
#  12 for multi_level_gemini_prompt_handler_v2  
#  13 for multi_level_claude_prompt_handler_v1 
#  14 for multi_level_claude_prompt_handler_v2  

# Model names
OPENAI_MODEL_NAME = "gpt-4o" 
GEMINI_MODEL_NAME = "gemini-1.5-pro"
CLAUDE_MODEL_NAME = "claude-3-5-sonnet-20241022"


### PT DATA SET PARSING FOR DR ###
PT_DATASET = 'semeval_PT_dataset_2'  # Name of the dataset containing persuasion techniques (PTs)
BATCH_SIZE = 1  # Number of parses to perform before saving the results
API_CALL_DELAY_SEC = 10  # Delay in seconds between each API call
RUN_DELAY_SEC = 60  # Delay in seconds after saving results (before the next batch)



