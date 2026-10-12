from app.schemas.models import UserIntent
from app.prompts.intent_prompt import INTENT_PROMPT
from openai import OpenAI

client = OpenAI()

def extract_user_intent(user_input: str, system_prompt: str = INTENT_PROMPT) -> UserIntent:
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": INTENT_PROMPT},
            {"role": "user", "content": user_input}
        ],
        text_format=UserIntent
    )
    
    if response.output_parsed is None:
        raise ValueError("Failed to parse the response into UserIntent.")
    
    return response.output_parsed