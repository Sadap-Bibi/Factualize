import requests
from bs4 import BeautifulSoup

def scrape_news():
    url = "https://www.bbc.com/news"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        headlines = []
        for item in soup.find_all('h3', class_='gs-c-promo-heading__title'):
            headlines.append(item.get_text())
        
        return headlines if headlines else ["No headlines found"]
    except requests.RequestException as e:
        print(f"Error scraping news: {e}")
        return ["Error fetching news"]