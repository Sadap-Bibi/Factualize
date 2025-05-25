import nltk
from nltk.tokenize import word_tokenize

def ensure_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("Downloading NLTK data...")
        try:
            nltk.download('punkt')
            nltk.download('punkt_tab')
            print("NLTK data downloaded successfully")
        except Exception as e:
            raise Exception(f"Failed to download NLTK data: {str(e)}")

def preprocess_text(text):
    ensure_nltk_data()
    try:
        tokens = word_tokenize(text.lower())
        # Keep all tokens, no stop word removal
        return ' '.join(tokens)
    except Exception as e:
        raise Exception(f"Text preprocessing failed: {str(e)}")