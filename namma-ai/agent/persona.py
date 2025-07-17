from typing import Literal

def detect_persona(user_input: str) -> Literal["tourist", "resident", "ambiguous", "unknown"]:
    tourist_keywords = [
        "weekend", "visiting", "visit", "2 days", "short trip", "sightseeing", "palace", "museum",
        "tourist", "attraction", "explore", "holiday", "trip", "next week", "this week", "places to see",
        "things to do", "must see", "must visit", "instagrammable", "photo spot"
    ]
    resident_keywords = [
        "moving", "relocating", "relocate", "shift", "shifting", "job", "work", "flat", "apartment", "rent",
        "stay", "living", "settle", "settling", "resident", "permanent", "long term", "next month",
        "i am shifting", "i am moving", "i am relocating", "move there", "move", "next year",
        "planning to move", "want to move", "thinking of moving"
    ]
    ambiguous_keywords = [
        "few months", "remote work", "thinking of staying", "trying it out", "explore for work",
        "part-time stay", "semi-permanent"
    ]

    input_lower = user_input.lower()
    if any(kw in input_lower for kw in tourist_keywords):
        return "tourist"
    elif any(kw in input_lower for kw in resident_keywords):
        return "resident"
    elif any(kw in input_lower for kw in ambiguous_keywords):
        return "ambiguous"
    else:
        return "unknown"