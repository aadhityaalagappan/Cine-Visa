
from dotenv import load_dotenv
load_dotenv()

import json
from pathlib import Path

from app.agents.taste_agent import analyse_taste
from app.agents.intent_agent import extract_user_intent
from app.agents.discovery_agent import discover_movies
from app.agents.similarity_agent import rank_movies
from app.agents.feedback_agent import update_taste


results = {
    "version": "V2",
    "description": "Refined system prompts"
}



taste_input = (
    "I loved Kara Para Ask because of its complex characters "
    "and emotional depth. I enjoyed the intricate plot twists "
    "and how the story kept me guessing. However, I disliked "
    "the slow pacing and lack of development for side characters. "
    "I loved the emotional connection and natural acting."
)

taste = analyse_taste(taste_input)

print("\n TASTE AGENT")
print(taste.model_dump_json(indent=2))

results["taste_agent"] = {
    "input": taste_input,
    "output": taste.model_dump()
}



intent_input = (
    "I want a series similar to Kara Para Ask, but with faster "
    "pacing and better side-character development. "
    "I prefer English or Spanish series. "
    "I want complex characters, emotional depth, "
    "and an engaging story."
)

intent = extract_user_intent(intent_input)

print("\nINTENT AGENT")
print(intent.model_dump_json(indent=2))

results["intent_agent"] = {
    "input": intent_input,
    "output": intent.model_dump()
}



discovery, movies = discover_movies(taste, intent)

print("\n DISCOVERY AGENT")
print(discovery.model_dump_json(indent=2))

for movie in movies:
    print(f"{movie.id}: {movie.title} ({movie.country})")

results["discovery_agent"] = {
    "output": discovery.model_dump(),
    "candidates": [
        movie.model_dump() for movie in movies
    ]
}



ranked = rank_movies(taste, intent, movies)

print("\nSIMILARITY AGENT")
print(ranked.model_dump_json(indent=2))

results["similarity_agent"] = {
    "output": ranked.model_dump()
}



feedback_input = (
    "I hate sloe pacing dramas, "
    "I want a horror drama to watch."
)

feedback = update_taste(taste, feedback_input)

print("\n FEEDBACK AGENT")
print(feedback.model_dump_json(indent=2))

results["feedback_agent"] = {
    "input": feedback_input,
    "output": feedback.model_dump()
}



new_intent = extract_user_intent(feedback_input)

print("\nNEW INTENT")
print(new_intent.model_dump_json(indent=2))

results["new_intent"] = {
    "input": feedback_input,
    "output": new_intent.model_dump()
}



sensitivity_inputs = [
    "I hate slow-paced dramas.",
    "I hate sloe pacing dramas.",
    "I lose interest when a series moves too slowly.",
    "I dislike slow pacing, but I want horror tonight.",
    "I usually dislike horror, but I want to try it tonight."
]

results["sensitivity_tests"] = []

for i, text in enumerate(sensitivity_inputs, start=1):

    feedback_result = update_taste(taste, text)
    intent_result = extract_user_intent(text)

    results["sensitivity_tests"].append({
        "test": i,
        "input": text,
        "feedback": feedback_result.model_dump(),
        "intent": intent_result.model_dump()
    })

    print(f"\nSENSITIVITY TEST {i}")
    print("Input:", text)
    print("Feedback:", feedback_result.model_dump_json(indent=2))
    print("Intent:", intent_result.model_dump_json(indent=2))



stability_input = (
    "I loved Kara Para Ask for its emotional depth "
    "and plot twists, but disliked its slow pacing."
)

results["stability_tests"] = []

for run in range(1, 4):

    output = analyse_taste(stability_input)

    results["stability_tests"].append({
        "run": run,
        "input": stability_input,
        "output": output.model_dump()
    })

    print(f"\n STABILITY RUN {run}")
    print(output.model_dump_json(indent=2))



output_path = Path("prompt_results_v2.json")

output_path.write_text(
    json.dumps(results, indent=2),
    encoding="utf-8"
)

print(f"\nResults saved to {output_path}")
