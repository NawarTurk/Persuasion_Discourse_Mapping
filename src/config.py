# API keys
OPENAI_API_KEY = ""
GEMINI_API_KEY = ""
CLAUDE_API_KEY = ""

# Prompt 
PROMPT_KEY = 'promptN07'  

#Delay
PROCESSING_DELAY_SECONDS = 3 # seconds

# Parser
PARSER_ID = 2# 
#  1 for the gpt_prompt_handler
#  2 for the gemini_prompt_handler   
#  3 for the claude_prompt_handler   


# Model names
OPENAI_MODEL_NAME = "gpt-4o" 
GEMINI_MODEL_NAME = "gemini-1.5-pro"  # or gemini-2.0-flash-exp'
CLAUDE_MODEL_NAME = "claude-3-5-sonnet-20241022"


### PT DATA SET PARSING FOR DR ###
PT_DATASET = 'PT_dataset_decreased'  # Name of the dataset containing persuasion techniques (PTs)
BATCH_SIZE = 40  # Number of parses to perform before saving the results
API_CALL_DELAY_SEC = 3  # Delay in seconds between each API call
RUN_DELAY_SEC = 50  # Delay in seconds after saving results (before the next batch)



