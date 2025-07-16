from agent.retriever import load_vector_store, query_guide
from agent.web_search import search_web
from agent.persona import detect_persona
from agent.prompts import get_prompt
from agent.llm_wrapper import generate_response_gemini

vdb = load_vector_store()

WEB_SEARCH_KEYWORDS = [
    "now", "today", "rent", "metro", "price", "live", "restaurant", "cafe", "bar", "eat", "drink", "dish", "cuisine", "food", "place", "timing", "rating", "menu", "best", "recommend"
]

# Helper for LLM-based persona detection

def llm_detect_persona(user_input: str) -> str:
    prompt = f"Is the user a tourist or a resident based on this message? Reply with only 'tourist', 'resident', or 'unknown'. Message: {user_input}"
    result = generate_response_gemini(prompt).strip().lower()
    if 'tourist' in result:
        return 'tourist'
    elif 'resident' in result:
        return 'resident'
    else:
        return 'unknown'

def explicit_persona_switch(user_input: str):
    lowered = user_input.lower()
    if 'switch to tourist' in lowered or 'tourist mode' in lowered:
        return 'tourist'
    if 'switch to resident' in lowered or 'resident mode' in lowered:
        return 'resident'
    return None

def generate_response(user_input: str, session_persona=None):
    # Check for explicit persona switch
    explicit = explicit_persona_switch(user_input)
    if explicit:
        persona = explicit
    else:
        detected_persona = detect_persona(user_input)
        if detected_persona == "unknown":
            detected_persona = llm_detect_persona(user_input)
        persona = detected_persona if detected_persona != "unknown" else session_persona or "unknown"

    context = query_guide(user_input, vdb)
    should_search = any(word in user_input.lower() for word in WEB_SEARCH_KEYWORDS)
    # Treat PDF as missing/outdated if context is empty or question is about current events
    pdf_missing = not context.strip() or should_search
    web_info = search_web(user_input) if should_search or pdf_missing else ""
    prompt = get_prompt(persona, context, web_info, user_input)
    response = generate_response_gemini(prompt)
    return response, persona
