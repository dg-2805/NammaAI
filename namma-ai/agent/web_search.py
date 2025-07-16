from ddgs import DDGS

def search_web(query: str, max_results=3):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        if results:
            formatted = []
            for r in results:
                snippet = r.get('body') or r.get('snippet') or ''
                formatted.append(f"{r['title']}: {r['href']}\n{snippet}")
            return "\n\n".join(formatted)
        return "No live results found."
