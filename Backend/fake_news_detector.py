from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_utils import preprocess_text
from collections import deque

def detect_fake_news(user_input, live_news, threshold=0.2):
    if not user_input or not live_news:
        raise ValueError("User input or live news list cannot be empty")
    
    try:
        processed_input = preprocess_text(user_input)
        processed_news = [preprocess_text(news) for news in live_news if news.strip()]
        
        print(f"Processed input: {processed_input}")
        print(f"Processed news (first 5): {processed_news[:5]}")
        print(f"Threshold: {threshold}")
        
        if not processed_news:
            raise ValueError("No valid news articles to compare against")
        if not processed_input:
            raise ValueError("Processed user input is empty")
        
        vectorizer = TfidfVectorizer()
        all_texts = [processed_input] + processed_news
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        tfidf_input = tfidf_matrix[0]
        tfidf_news = tfidf_matrix[1:]
        
        original_news = [news for news in live_news if news.strip()]
        all_similarities = []
        news_pairs = []
        
        for idx, tfidf_news_item in enumerate(tfidf_news):
            similarity = cosine_similarity(tfidf_input, tfidf_news_item).flatten()[0]
            all_similarities.append(similarity)
            news_pairs.append((similarity, original_news[idx]))
        
        print(f"All similarities: {all_similarities}")
        print(f"News pairs (first 5): {news_pairs[:5]}")
        
        max_similarity = max(all_similarities)
        is_fake = max_similarity < threshold
        confidence = max_similarity
        
        closest_headline = max(news_pairs, key=lambda x: x[0])[1] if news_pairs else "No matching headline found."
        print(f"Closest headline (similarity {max_similarity}): {closest_headline}")
        
        return {
            "similarity": float(max_similarity),
            "is_fake": bool(is_fake),
            "confidence": float(confidence),
            "summary": closest_headline,
            "similarity_scores": all_similarities
        }
    except Exception as e:
        raise Exception(f"Fake news detection failed: {str(e)}")