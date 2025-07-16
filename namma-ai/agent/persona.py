from typing import Literal

def detect_persona(user_input: str) -> Literal["tourist", "resident", "unknown"]:
    tourist_keywords = [
        "weekend", "visiting", "visit", "2 days", "short trip", "sightseeing", "palace", "museum", "tourist", "attraction", "explore", "holiday", "trip", "next week", "this week", "see", "places to see", "things to do"
    ]
    resident_keywords = [
        "moving", "relocating", "relocate", "shift", "shifting", "job", "work", "flat", "apartment", "rent", "stay", "living", "settle", "settling", "resident", "permanent", "long term", "next month", "i am shifting", "i am moving", "i am relocating", "move there", "move", "next year", "planning to move", "want to move", "thinking of moving"
    ]

    input_lower = user_input.lower()
    if any(word in input_lower for word in tourist_keywords):
        return "tourist"
    elif any(word in input_lower for word in resident_keywords):
        return "resident"
    else:
        return "unknown"
