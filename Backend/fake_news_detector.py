from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_utils import preprocess_text

def detect_fake_news(user_input, live_news, threshold=0.5):
    if not user_input or not live_news:
        raise ValueError("User input or live news list cannot be empty")
    
    try:
        processed_input = preprocess_text(user_input)
        processed_news = [preprocess_text(news) for news in live_news if news.strip()]
        
        print(f"Processed input: {processed_input}")
        print(f"Processed news: {processed_news}")
        
        if not processed_news:
            raise ValueError("No valid news articles to compare against")
        if not processed_input:
            raise ValueError("Processed user input is empty")
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([processed_input] + processed_news)
        
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        max_similarity = max(similarities)
        
        print(f"Similarity scores: {similarities}")
        
        is_fake = max_similarity < threshold
        confidence = max_similarity * 100
        
        # Find the index of the highest similarity score
        max_similarity_index = similarities.argmax()
        closest_headline = live_news[max_similarity_index] if not is_fake else None
        
        return {
            "is_fake": bool(is_fake),
            "confidence": float(confidence),
            "summary": generate_summary(user_input),  # Kept for potential future use
            "similarity_scores": similarities.tolist(),
            "closest_headline": closest_headline  # Closest matching headline
        }
    except Exception as e:
        raise Exception(f"Fake news detection failed: {str(e)}")

def generate_summary(text, num_sentences=2):
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    import string
    
    try:
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return " ".join(sentences)
        
        stop_words = set(stopwords.words('english') + list(string.punctuation))
        words = word_tokenize(text.lower())
        word_freq = {word: words.count(word) for word in set(words) if word not in stop_words and word.isalnum()}
        
        sentence_scores = {}
        for sentence in sentences:
            for word, freq in word_freq.items():
                if word in sentence.lower():
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq
        
        sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        top_sentences = [sentence for sentence, _ in sorted_sentences[:num_sentences]]
        summary_sentences = [sent for sent in sentences if sent in top_sentences]
        
        return " ".join(summary_sentences) if summary_sentences else "Unable to generate summary."
    except Exception as e:
        return f"Summary generation failed: {str(e)}"