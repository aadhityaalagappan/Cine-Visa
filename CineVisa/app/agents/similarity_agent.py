import json
from openai import OpenAI
from app.schemas.models import TasteProfile, UserIntent, Movie, DiscoveryResult, SimilarityResult
from app.prompts.similarity_prompt import SIMILARITY_PROMPT

client = OpenAI()

def rank_movies(taste: TasteProfile, intent: UserIntent, candidates: list[Movie], system_prompt: str = SIMILARITY_PROMPT) -> SimilarityResult:
    if not candidates:
        return SimilarityResult(recommendations=[])
    
    
    context = {
        "taste": taste.model_dump(),
        "intent": intent.model_dump(),
        "candidates": [movie.model_dump() for movie in candidates]
    }
    
    response = client.responses.parse(
        
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SIMILARITY_PROMPT},
            {"role": "user", "content": json.dumps(context)}
        ],
        text_format=SimilarityResult
        
    )
    
    if response.output_parsed is None:
        raise ValueError("Similarity Agent returned no output") 
    
    result = response.output_parsed
    
    valid_ids = [movie.id for movie in candidates]
    
    valid_movie_matches = []
    
    seen_movie_ids = set()
    
    for recommendation in result.recommendations:
        if recommendation.movie_id in valid_ids and recommendation.movie_id not in seen_movie_ids:
            valid_movie_matches.append(recommendation)
            seen_movie_ids.add(recommendation.movie_id)
            
    result.recommendations = sorted(valid_movie_matches, key= lambda x: x.score, reverse=True)[:3]
    
    return result        

