"""
NammaAI Agent Core Module

This module contains the main orchestration logic for the NammaAI Bangalore concierge.
It handles persona detection, context retrieval from PDF and web sources, and response generation.
"""

from typing import Optional, Tuple, List
from agent.retriever import load_vector_store, query_guide
from agent.web_search import search_web
from agent.persona import detect_persona
from agent.prompts import get_prompt
from agent.llm_wrapper import generate_response_gemini
import re
import random

vdb = load_vector_store()

WEB_SEARCH_KEYWORDS = [
    "now", "today", "rent", "metro", "price", "live", "restaurant", "cafe", "bar", "eat", "drink", "dish",
    "cuisine", "food", "place", "timing", "rating", "menu", "best", "recommend", "sushi", "pizza",
    "biryani", "hours", "open", "closed", "current", "latest", "new", "popular", "reviews", "address",
    "location", "phone", "contact", "delivery", "takeaway", "dine", "book", "reservation",
    "instagrammable", "selfie", "photo spot"
]

def llm_detect_persona(user_input: str) -> str:
    """
    Use LLM to detect user persona when rule-based detection fails.
    
    Args:
        user_input: User's message
        
    Returns:
        Detected persona: 'tourist', 'resident', 'ambiguous', or 'unknown'
    """
    prompt = f"Classify the following message as 'tourist', 'resident', or 'ambiguous'. Be strict.\nMessage: {user_input}"
    result = generate_response_gemini(prompt).strip().lower()
    for value in ["tourist", "resident", "ambiguous"]:
        if value in result:
            return value
    return "unknown"

def explicit_persona_switch(user_input: str) -> Optional[str]:
    """
    Check if user explicitly requests to switch persona mode.
    
    Args:
        user_input: User's message
        
    Returns:
        'tourist', 'resident', or None if no explicit switch requested
    """
    lowered = user_input.lower()
    if 'switch to tourist' in lowered or 'tourist mode' in lowered:
        return 'tourist'
    if 'switch to resident' in lowered or 'resident mode' in lowered:
        return 'resident'
    return None

def needs_web_search(user_input: str) -> bool:
    """
    Determines if web search should be triggered to supplement PDF context.
    Web search is used for current/dynamic information, not to replace PDF context.
    """
    return any(keyword in user_input.lower() for keyword in WEB_SEARCH_KEYWORDS)

def generate_response(user_input: str, session_persona: Optional[str] = None, conversation_history: Optional[List[str]] = None) -> Tuple[str, str]:
    """
    Generate AI response using persona detection, PDF context, and web search.
    
    Args:
        user_input: User's question or message
        session_persona: Previously detected persona for the session
        conversation_history: List of recent conversation exchanges
        
    Returns:
        Tuple of (response_text, detected_persona)
    """
    explicit = explicit_persona_switch(user_input)
    if explicit:
        persona = explicit
    else:
        detected_persona = detect_persona(user_input)
        if detected_persona == "unknown":
            detected_persona = llm_detect_persona(user_input)
        persona = detected_persona if detected_persona != "unknown" else session_persona or "unknown"

    # Always get PDF context from the city guide
    # For fallback, get only the most relevant chunk (k=1)
    context = query_guide(user_input, vdb, k=1)
    
    # Add web search for current/dynamic information when needed
    web_info = search_web(user_input) if needs_web_search(user_input) else ""

    prompt = get_prompt(persona, context, web_info, user_input, conversation_history)
    response = generate_response_gemini(prompt)
    if response == "__LLM_ERROR__":
        # Extract main keywords from user_input (longest word > 3 chars, or all words > 3 chars)
        keywords = [w for w in re.findall(r'\w+', user_input) if len(w) > 3]
        # Split the chunk into sentences
        sentences = re.split(r'(?<=[.!?])\s+', context.strip())
        # Find sentences mentioning any keyword (case-insensitive)
        relevant = [s for s in sentences if any(k.lower() in s.lower() for k in keywords)]
        # If none found, fallback to first 2-3 sentences
        if not relevant:
            relevant = sentences[:3]
        # Limit to 2-3 sentences for brevity
        short_answer = ' '.join(relevant[:3]).strip()
        fallback = short_answer or "Sorry, no relevant information found in the city guide."
        kannada_phrases = [
            "Namaskara (Hello)",
            "Dhanyavadagalu (Thank you)",
            "Meter haaki (Turn on the meter)"
        ]
        phrase = random.choice(kannada_phrases)
        fallback_msg = f"The city guide states: {fallback}\n\nKannada phrase: {phrase}"
        return fallback_msg, persona
    return response, persona