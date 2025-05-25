import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor

headline_cache = {}
last_fetched = 0
CACHE_DURATION = 1800  # 30 minutes

NEWS_SOURCES = {
    'bbc': {
        'url': 'https://www.bbc.com/news',
        'selectors': ['h1, h2, h3, a[href*="/news/"]'],  # Multiple selectors
        'min_length': 20
    },
    'the_hindu': {
        'url': 'https://www.thehindu.com',
        'selectors': ['h1, h2, h3, .title a, a.story-card-news'],  # Broader selectors
        'min_length': 20
    },
    'times_of_india': {
        'url': 'https://timesofindia.indiatimes.com',
        'selectors': ['h1, h2, h3, a[href*="/articleshow/"], .top-story a'],  # Broader selectors
        'min_length': 20
    }
}

def scrape_single_source(source_name, config):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(config['url'], headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        headlines = []
        for selector in config['selectors']:
            elements = soup.select(selector)
            for item in elements:
                text = item.get_text(strip=True)
                if len(text) >= config['min_length'] and text not in headlines:
                    headlines.append(text)
        
        # Remove duplicates while preserving order
        headlines = list(dict.fromkeys(headlines))
        
        print(f"Found {len(headlines)} headlines from {source_name}: {headlines[:5]}")
        return headlines
    except requests.RequestException as e:
        print(f"Error scraping {source_name}: {e}")
        return []

def scrape_news():
    global last_fetched
    current_time = time.time()

    if current_time - last_fetched < CACHE_DURATION and headline_cache:
        print("Using cached headlines")
        return list(headline_cache.values())

    all_headlines = []
    
    with ThreadPoolExecutor(max_workers=len(NEWS_SOURCES)) as executor:
        future_to_source = {executor.submit(scrape_single_source, name, config): name 
                           for name, config in NEWS_SOURCES.items()}
        
        for future in future_to_source:
            source_name = future_to_source[future]
            try:
                headlines = future.result()
                if headlines:
                    all_headlines.extend(headlines)
                    print(f"Successfully scraped {source_name}: {len(headlines)} headlines")
            except Exception as e:
                print(f"Error processing {source_name}: {e}")

    if not all_headlines:
        print("No headlines found, using fallback headlines")
        all_headlines = [
            "Scientists discover new species in Pacific Ocean.",
            "Global leaders meet to discuss climate change.",
            "New technology boosts renewable energy production.",
            "Major breakthrough in renewable energy storage.",
            "International cooperation leads to medical advancement."
        ]

    # Remove duplicates and sort by length
    all_headlines = list(dict.fromkeys(all_headlines))
    all_headlines.sort(key=len)
    
    # Update cache
    headline_cache.clear()
    for i, headline in enumerate(all_headlines):
        headline_cache[i] = headline
    last_fetched = current_time

    print(f"Total headlines gathered: {len(all_headlines)}, Sample: {all_headlines[:5]}")
    return all_headlines

if __name__ == "__main__":
    headlines = scrape_news()
    for idx, headline in enumerate(headlines, 1):
        print(f"{idx}. {headline}")