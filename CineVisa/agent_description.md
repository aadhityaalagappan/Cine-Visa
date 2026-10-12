# CinePassport — AI Agents Overview

## 1. Taste Agent
**Description:** Understands the user's long-term movie and series preferences and creates their Taste DNA. Updates preferences based on feedback.

**Example:** "I love Kara Para Aşk for its romance and suspense, and Drishyam for its unexpected twists."

**Output:** Prefers romance, thrillers, suspense, and unexpected twists.

## 2. Intent Agent
**Description:** Understands what the user wants to watch right now, considering their current request and saved Taste DNA.

**Example:** "Recommend a romance series similar to Kara Para Aşk, but from another country."

**Output:** Looking for an international romance series with similar story elements.

## 3. Discovery Agent
**Description:** Searches movie databases like TMDb to find movies and series matching the user's request.

**Example:** Searches for romance series with crime, mystery, and emotional relationships.

**Output:** Candidate series such as Siyah Beyaz Aşk and Cesur ve Güzel.

## 4. Context Agent
**Description:** Retrieves actual story information about discovered titles, including plot, characters, themes, and relationships.

**Example:** Analyzes Siyah Beyaz Aşk to identify its romantic storyline, character conflicts, and suspense elements.

**Output:** Structured story details used for comparison.

## 5. Similarity Agent
**Description:** Compares discovered titles with the user's current request and Taste DNA to rank the best matches.

**Example:** Compares Siyah Beyaz Aşk with Kara Para Aşk based on romance, suspense, and character relationships.

**Output:** Ranked recommendations with explanations of why each series matches.

## 6. Feedback Agent
**Description:** Analyzes user ratings and comments to identify likes and dislikes, then sends these insights to the Taste Agent to update Taste DNA.

**Example:** "I loved the chemistry between the leads and the suspense."

**Output:** Adds romantic chemistry and suspense as positive preference signals.

---

## Overall Workflow

**Recommendation Flow:**

Taste DNA + User Query → Intent Agent → Discovery Agent → Context Agent → Similarity Agent → Recommendations

**Feedback Flow:**

User Feedback → Feedback Agent → Taste Agent → Updated Taste DNA