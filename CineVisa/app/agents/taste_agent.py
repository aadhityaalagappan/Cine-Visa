from openai import OpenAI
from app.schemas.models import TasteProfile
from app.prompts.taste_prompt import TASTE_PROMPT

client = OpenAI()

def analyse_taste(user_input: str, system_prompt: str = TASTE_PROMPT) -> TasteProfile:
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": TASTE_PROMPT},
            {"role": "user", "content": user_input}
        ],
        text_format=TasteProfile
    )
    
    if response.output_parsed is None:
        raise ValueError("Failed to parse the response into TasteProfile.")
    
    return response.output_parsed   

