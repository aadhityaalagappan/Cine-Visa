import json
from openai import OpenAI

from app.schemas.models import TasteProfile, FeedbackResult
from app.prompts.feedback_prompt import FEEDBACK_PROMPT

client = OpenAI()


def unique_traits(traits: list[str]) -> list[str]:
    seen = set()
    result = []

    for trait in traits:
        normalized = trait.strip().lower()

        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)

    return result


def update_taste(
    taste: TasteProfile,
    feedback: str,
    system_prompt: str = FEEDBACK_PROMPT
) -> FeedbackResult:

    context = {
        "current_taste": taste.model_dump(),
        "feedback": feedback
    }

    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": FEEDBACK_PROMPT},
            {"role": "user", "content": json.dumps(context)}
        ],
        text_format=FeedbackResult
    )

    result = response.output_parsed

    if result is None:
        raise ValueError("Feedback Agent returned no output")

    result.updated_taste.liked_traits = unique_traits(
        result.updated_taste.liked_traits
    )

    result.updated_taste.disliked_traits = unique_traits(
        result.updated_taste.disliked_traits
    )

    old_likes = {
        trait.strip().lower()
        for trait in taste.liked_traits
    }

    old_dislikes = {
        trait.strip().lower()
        for trait in taste.disliked_traits
    }

    result.liked_traits = [
        trait
        for trait in result.updated_taste.liked_traits
        if trait.lower() not in old_likes
    ]

    result.disliked_traits = [
        trait
        for trait in result.updated_taste.disliked_traits
        if trait.lower() not in old_dislikes
    ]

    return result