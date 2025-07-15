# search_google.py

import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    raise Exception("❌ SERPAPI_KEY not found. Check your .env file.")

print(f"🔑 API Key Loaded: {API_KEY[:8]}...")

def search_outdoor_companies(search_term, location="Montana"):
    params = {
        "engine": "google",
        "q": f"{search_term} {location}",
        "api_key": API_KEY,
        "num": 20
    }

    search = GoogleSearch(params)
    results = search.get_dict().get("organic_results", [])
    urls = []

    for result in results:
        link = result.get("link")
        title = result.get("title", "")
        if link and "linkedin" not in link and "facebook" not in link:
            urls.append({"title": title, "link": link, "term": search_term})
    
    return urls