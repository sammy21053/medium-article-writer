import requests

def get_trending_ai_topics(api_key):
    """
    Fetches current trending tech/AI-related search queries
    """
    url = "https://google.serper.dev/search"
    payload = {
        "q": "AI OR artificial intelligence OR machine learning OR tech trends 2025",
        "gl": "US",
        "type": "search"
    }
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        # Extract top related queries
        related_queries = [item['query'] for item in data.get('relatedSearches', [])[:5]]
        return related_queries
    except Exception as e:
        print("Error fetching trending topics:", e)
        return []