from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_utils import preprocess_text
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string

def detect_fake_news(user_input, live_news):
    try:
        processed_input = preprocess_text(user_input)
        processed_news = [preprocess_text(news) for news in live_news]
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([processed_input] + processed_news)
        
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        max_similarity = max(similarities)
        
        is_fake = max_similarity < 0.7
        confidence = max_similarity * 100
        
        return {
            "is_fake": is_fake,
            "confidence": round(confidence, 2),
            "summary": generate_summary(user_input),
            "similarity_scores": similarities.tolist()
        }
    except Exception as e:
        raise Exception(f"Fake news detection failed: {str(e)}")

def generate_summary(text, num_sentences=2):
    try:
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return " ".join(sentences)
        
        stop_words = set(stopwords.words('english') + list(string.punctuation))
        words = word_tokenize(text.lower())
        word_freq = {}
        
        for word in words:
            if word not in stop_words and word.isalnum():
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sentence_scores = {}
        for sentence in sentences:
            for word, freq in word_freq.items():
                if word in sentence.lower():
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq
        
        sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        top_sentences = [sentence for sentence, score in sorted_sentences[:num_sentences]]
        summary_sentences = [sent for sent in sentences if sent in top_sentences]
        
        return " ".join(summary_sentences) if summary_sentences else "Unable to generate summary."
    except Exception as e:
        return f"Summary generation failed: {str(e)}"