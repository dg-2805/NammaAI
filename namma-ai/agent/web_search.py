import serpapi
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable
SERP_API_KEY = os.getenv("SERP_API_KEY")
if not SERP_API_KEY:
    raise ValueError("SERP_API_KEY environment variable not set.")

def search_web(query: str, max_results=3, location: str = "Bangalore, India"):
    """
    Use SerpAPI Google Search and BeautifulSoup to perform enhanced web search.
    Augments search based on query context and scrapes brief snippets from top URLs.
    """
    try:
        query_lower = query.lower()
        # Ensure location context
        if 'bangalore' not in query_lower and 'bengaluru' not in query_lower:
            query += " Bangalore"

        # Detect if query is about food to limit search to food platforms
        food_keywords = ['restaurant', 'cafe', 'bar', 'food', 'eat', 'drink', 'cuisine', 'dish', 'menu']
        is_restaurant_query = any(k in query_lower for k in food_keywords)

        if is_restaurant_query:
            # Focus on popular food websites in Bangalore for richer content
            search_query = f"{query} site:zomato.com OR site:magicpin.in OR site:swiggy.com"
        else:
            # General Bangalore queries use official/local tourism or info sites
            search_query = f"{query} site:mybengaluru.com OR site:tripadvisor.com OR site:bengaluru.gov.in OR site:karnatakatourism.org"

        # Set up the SerpAPI search
        search = serpapi.GoogleSearch({
            "q": search_query,
            "location": location,
            "hl": "en",
            "gl": "in",
            "api_key": SERP_API_KEY
        })

        results = search.get_dict()

        # Defensive: organic_results may not be present or could be empty
        organic_results = results.get("organic_results", [])
        if not organic_results:
            return "No organic search results found."

        # Extract target URLs, up to max_results
        links = [r.get('link') for r in organic_results if r.get('link')]
        links = links[:max_results]

        # Scrape each link and extract a clean snippet preview (~400 chars)
        snippets = []
        headers = {"User-Agent": "Mozilla/5.0 (compatible; NammaAI/1.0)"}

        for url in links:
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, 'html.parser')
                # Extract visible text, join with spaces, strip excessive whitespace
                text = soup.get_text(separator=' ', strip=True)
                snippet = text[:400] + "..." if len(text) > 400 else text

                snippets.append(f"📍 {url}\n📝 {snippet}")
            except Exception as e:
                snippets.append(f"❌ Failed to fetch {url}: {str(e)}")

        return "\n\n".join(snippets) if snippets else "No results found."

    except Exception as e:
        # Catch network or API errors
        return f"❌ Web search failed: {str(e)}"
