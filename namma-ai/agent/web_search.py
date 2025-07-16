from ddgs import DDGS
import time

def search_web(query: str, max_results=5):
    """Search the web for Bangalore-specific data and extract concise, structured snippets"""
    try:
        if 'bangalore' not in query.lower() and 'bengaluru' not in query.lower():
            query = f"{query} Bangalore"
        
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            if results:
                cafes = []
                for i, r in enumerate(results, 1):
                    title = r.get("title", "").strip()
                    snippet = r.get("body") or r.get("snippet") or ""
                    snippet = snippet[:200] + "..." if len(snippet) > 200 else snippet

                    # Try to extract a clean name from title
                    if " - " in title:
                        name = title.split(" - ")[0]
                    else:
                        name = title
                    
                    cafes.append(f"• {name}\n  Details: {snippet}")
                return "\n".join(cafes)
            return ""
    except Exception as e:
        return f"Web search failed: {str(e)}"
