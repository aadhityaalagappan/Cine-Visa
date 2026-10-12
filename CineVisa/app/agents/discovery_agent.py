import json
from pathlib import Path
from openai import OpenAI

from app.schemas.models import TasteProfile, UserIntent, Movie, DiscoveryResult
from app.prompts.discovery_prompt import DISCOVERY_PROMPT

client = OpenAI()


def discover_movies(
    taste: TasteProfile,
    intent: UserIntent,
    system_prompt: str = DISCOVERY_PROMPT
) -> tuple[DiscoveryResult, list[Movie]]:

    path = Path("app/data/sample_movies.json") # Later I need to get the movies from the tmdb API instead of a local file

    with open(path, "r") as file:
        data = json.load(file)

    movies = [Movie(**item) for item in data]

    eligible = []

    for movie in movies:

        if intent.max_episodes is not None:
            if movie.episode_count is None or movie.episode_count > intent.max_episodes:
                continue

        if movie.language.lower() in [
            lang.lower() for lang in intent.excluded_languages
        ]:
            continue

        if intent.preferred_languages:
            if movie.language.lower() not in [
                lang.lower() for lang in intent.preferred_languages
            ]:
                continue

        if movie.title.lower() in [
            title.lower() for title in taste.favorite_titles
        ]:
            continue

        eligible.append(movie)

    context = {
        "taste": taste.model_dump(),
        "intent": intent.model_dump(),
        "movies": [movie.model_dump() for movie in eligible]
    }

    response = client.responses.parse(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": DISCOVERY_PROMPT},
            {"role": "user", "content": json.dumps(context)}
        ],
        text_format=DiscoveryResult
    )

    result = response.output_parsed

    if result is None:
        raise ValueError("Discovery Agent returned no output")

    candidates = []

    for movie in eligible:
        if movie.id in result.candidate_ids:
            candidates.append(movie)

    candidates = candidates[:5]
    result.candidate_ids = [movie.id for movie in candidates]

    return result, candidates