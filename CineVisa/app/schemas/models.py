from typing import Literal
from pydantic import BaseModel, Field


class TasteProfile(BaseModel):
    favorite_titles: list[str]
    disliked_titles: list[str] = []
    liked_traits: list[str]
    disliked_traits: list[str]
    liked_trait_details: list[str] = []     
    disliked_trait_details: list[str] = []  
    unknowns: list[str] = []
    needs_more_info: bool = False
    follow_up_questions: list[str] = []     
    reasoning: str
    self_check_passed: bool
    self_check_notes: str = ""


class UserIntent(BaseModel):
    request_type: Literal[
        "cross_culture_discovery", "similar_story", "series_discovery",
        "genre_exploration", "general_discovery",
    ]
    request_type_reason: str = ""
    reference_titles: list[str]
    desired_traits: list[str]
    excluded_traits: list[str]             
    must_have: list[str] = []
    nice_to_have: list[str] = []
    mood_or_tone: list[str] = []
    content_format: Literal["movie", "series", "either"] = "either"
    preferred_languages: list[str]
    excluded_languages: list[str]
    language_relation: Literal["same", "different", "any"] = "any"
    max_episodes: int | None
    conflicts_with_taste: str | None = None
    clarifying_questions: list[str] = []  
    explanation: str
    self_check_passed: bool
    self_check_notes: str = ""


class Movie(BaseModel):
    id: int
    title: str
    country: str
    language: str
    genres: list[str]
    overview: str
    story_traits: list[str]
    episode_count: int | None = None
    content_type: Literal["movie", "series"] | None = None
    pacing: str | None = None               


class DiscoveryResult(BaseModel):
    candidate_ids: list[int]
    candidate_titles: list[str] = []
    why_selected: list[str] = []
    matched_traits: list[str] = []
    caveats: list[str] = []
    language_check: list[Literal["pass", "fail", "unknown"]] = []
    episode_check: list[Literal["pass", "fail", "unknown"]] = []
    exclusion_check: list[Literal["pass", "fail", "unknown"]] = []
    near_miss_ids: list[int] = []          
    near_miss_reasons: list[str] = []
    search_reason: str
    self_check_passed: bool
    self_check_notes: str = ""


class MovieMatch(BaseModel):
    movie_id: int
    rank: int = Field(ge=1, le=3)
    title: str
    score: int = Field(ge=0, le=100)        
    story_fit: int | None = None           
    character_fit: int | None = None
    pacing_fit: int | None = None
    emotional_fit: int | None = None
    constraint_fit: int | None = None
    matched_liked_traits: list[str] = []
    conflicting_disliked_traits: list[str] = []
    caveats: list[str] = []
    confidence: Literal["low", "medium", "high"] = "medium"
    explanation: str


class SimilarityResult(BaseModel):
    recommendations: list[MovieMatch]
    comparison_note: str | None = None       
    self_check_passed: bool
    self_check_notes: str = ""


class FeedbackResult(BaseModel):
    liked_traits: list[str]                
    disliked_traits: list[str]             
    liked_trait_details: list[str] = []
    disliked_trait_details: list[str] = []
    changed_preferences: list[str] = []
    updated_taste: TasteProfile
    current_intent: str | None = None
    ambiguous_statements: list[str] = []
    explanation: str
    self_check_passed: bool
    self_check_notes: str = ""