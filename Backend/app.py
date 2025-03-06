from flask import Flask, request, jsonify
from flask_cors import CORS
print("Importing scraper and fake_news_detector")
from scraper import scrape_news
from fake_news_detector import detect_fake_news
print("Imports successful")
print("Checking NLTK data via nlp_utils")
from nlp_utils import preprocess_text
print("NLTK check complete")

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def detect():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        user_input = request.json.get('text')
        if not user_input or not isinstance(user_input, str):
            return jsonify({"error": "No valid text provided"}), 400
        
        live_news = scrape_news()
        result = detect_fake_news(user_input, live_news)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)