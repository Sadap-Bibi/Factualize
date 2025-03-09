from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp_utils import preprocess_text
from collections import defaultdict
import heapq
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string

# BST Implementation
class BSTNode:
    def __init__(self, value, headline):
        self.value = value  # Similarity score
        self.headline = headline
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value, headline):
        if not self.root:
            self.root = BSTNode(value, headline)
        else:
            self._insert(self.root, value, headline)

    def _insert(self, node, value, headline):
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value, headline)
            else:
                self._insert(node.left, value, headline)
        else:
            if node.right is None:
                node.right = BSTNode(value, headline)
            else:
                self._insert(node.right, value, headline)

    def inorder(self, node, result):
        if node:
            self.inorder(node.left, result)
            result.append((node.value, node.headline))
            self.inorder(node.right, result)

    def get_top_k(self, k):
        result = []
        self.inorder(self.root, result)
        return result[-k:][::-1]  # Top k in descending order

# Graph and DFS Implementation
def build_similarity_graph(live_news, similarity_threshold=0.7):
    processed_news = [preprocess_text(news) for news in live_news if news.strip()]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_news)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    graph = defaultdict(list)
    for i in range(len(live_news)):
        for j in range(i + 1, len(live_news)):
            if similarity_matrix[i][j] > similarity_threshold:
                graph[i].append(j)
                graph[j].append(i)
    return graph, processed_news

def dfs(graph, start, visited):
    visited.add(start)
    cluster = [start]
    for neighbor in graph[start]:
        if neighbor not in visited:
            cluster.extend(dfs(graph, neighbor, visited))
    return cluster

def check_cluster(user_input, live_news, graph, processed_news):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([preprocess_text(user_input)] + processed_news)
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    max_idx = similarities.argmax()
    connection_threshold = 0.5
    if similarities[max_idx] > connection_threshold:
        visited = set()
        cluster = dfs(graph, max_idx, visited)
        return len(cluster) > 2, len(cluster)  # Credible if cluster size > 2
    return False, 0

# Main Detection Function with BST and Heap
def detect_fake_news(user_input, live_news, threshold=0.5):
    if not user_input or not live_news:
        raise ValueError("User input or live news list cannot be empty")
    
    try:
        processed_input = preprocess_text(user_input)
        processed_news = [preprocess_text(news) for news in live_news if news.strip()]
        
        if not processed_news:
            raise ValueError("No valid news articles to compare against")
        if not processed_input:
            raise ValueError("Processed user input is empty")
        
        # Build graph and check cluster
        graph, processed_news = build_similarity_graph(live_news)
        is_clustered, cluster_size = check_cluster(user_input, live_news, graph, processed_news)
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([processed_input] + processed_news)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        # Use BST for all similarities
        bst = BST()
        for score, headline in zip(similarities, live_news):
            bst.insert(score, headline)
        
        # Use Heap for top-k
        heap = []
        for score, headline in zip(similarities, live_news):
            heapq.heappush(heap, (score, headline))
            if len(heap) > 3:  # Keep top 3
                heapq.heappop(heap)
        
        top_3_heap = sorted(heap, reverse=True)  # Convert heap to list in descending order
        top_3_bst = bst.get_top_k(3)  # Get top 3 from BST
        max_similarity = max(similarities) if similarities.size > 0 else 0
        
        is_fake = max_similarity < threshold
        confidence = max_similarity * 100
        
        closest_headline = top_3_heap[0][1] if top_3_heap and not is_fake else None
        
        return {
            "is_fake": bool(is_fake),
            "confidence": float(confidence),
            "summary": generate_summary(user_input),
            "similarity_scores": similarities.tolist(),
            "closest_headline": closest_headline,
            "top_matches_heap": [(float(score), headline) for score, headline in top_3_heap],
            "top_matches_bst": [(float(score), headline) for score, headline in top_3_bst],
            "is_clustered": bool(is_clustered),
            "cluster_size": int(cluster_size)
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