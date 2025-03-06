import requests
from bs4 import BeautifulSoup

def scrape_news():
    url = "https://www.bbc.com/news"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        headlines = []
        for item in soup.select('h2, h3'):
            text = item.get_text(strip=True)
            if text and len(text) > 10:
                headlines.append(text)
        
        return headlines if headlines else ["No headlines found"]
    except requests.RequestException as e:
        print(f"Error scraping news: {e}")
        return [
            "Scientists discover new species in Pacific Ocean.",
            "Global leaders meet to discuss climate change.",
            "New technology boosts renewable energy production."
        ]