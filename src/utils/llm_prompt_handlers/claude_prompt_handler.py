import anthropic
import config

#from Project.Persuasion_Discourse_Mapping.src.utils.llm_prompt_handlers.gemini_prompt_handler import api_key

model_name = config.CLAUDE_MODEL_NAME

def claude_prompt_handler(paragraph, prompt_template):
    prompt = prompt_template.format(paragraph=paragraph)

    client = anthropic.Anthropic(api_key=config.CLAUDE_API_KEY)
    message = client.messages.create(
        model=model_name,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    # print(message)

    return message.content[0].text.strip()