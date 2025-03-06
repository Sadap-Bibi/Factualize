import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Download NLTK data only if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')  # Legacy punkt
    nltk.data.find('tokenizers/punkt_tab')  # New tabular punkt
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('punkt')  # Downloads legacy punkt
    nltk.download('punkt_tab')  # Downloads new tabular punkt
    nltk.download('stopwords')
    print("NLTK data downloaded successfully")

def preprocess_text(text):
    # Tokenize and remove stopwords/punctuation
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return ' '.join(tokens)