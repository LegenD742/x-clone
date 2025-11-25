import requests
from bs4 import BeautifulSoup
import time
import random

DUCK_URL = "https://html.duckduckgo.com/html/"


USER_AGENTS = [
    
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36",

    
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:114.0) Gecko/20100101 Firefox/114.0",

    
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15 Safari/605.1.15",


    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36 Edg/118.0",
]


def duckduckgo_search(query, max_results=10):
    """
    Perform DuckDuckGo HTML search using POST request.
    Returns cleaned GitHub links.
    """

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
    }

    payload = {"q": query}

    try:
        time.sleep(random.uniform(0.7, 1.6))

        response = requests.post(DUCK_URL, data=payload, headers=headers, timeout=7)
        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for a in soup.select("a.result__a"):
            url = a.get("href")
            if url and "github.com" in url:
                links.append(url)
            if len(links) >= max_results:
                break

        return links

    except Exception as e:
        print("DuckDuckGo error:", e)
        return []
