import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

def ensure_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading NLTK data...")
        try:
            nltk.download('punkt')
            nltk.download('punkt_tab')
            nltk.download('stopwords')
            print("NLTK data downloaded successfully")
        except Exception as e:
            raise Exception(f"Failed to download NLTK data: {str(e)}")

def preprocess_text(text):
    ensure_nltk_data()
    try:
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        return ' '.join(tokens)
    except Exception as e:
        raise Exception(f"Text preprocessing failed: {str(e)}")