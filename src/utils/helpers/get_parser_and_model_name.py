import config
from utils.llm_prompt_handlers.claude_prompt_handler import claude_prompt_handler
from utils.llm_prompt_handlers.gemini_prompt_handler import gemini_prompt_handler
from utils.llm_prompt_handlers.gpt_prompt_handler import gpt_prompt_handler


def get_parser_and_model_name(parser_id):
    # Dictionary to map parser_id to their corresponding parser handler and model name
        parser_config = {
            1: (gpt_prompt_handler, config.OPENAI_MODEL_NAME),
            2: (gemini_prompt_handler, config.GEMINI_MODEL_NAME),
            3: (claude_prompt_handler, config.CLAUDE_MODEL_NAME),
        }

        if parser_id in parser_config:
            parser, model_name = parser_config[parser_id]
            return parser, model_name
        else:
            raise ValueError("Invalid parser id provided.")