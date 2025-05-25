from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_news
from fake_news_detector import detect_fake_news
from nlp_utils import preprocess_text

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "http://localhost:3000"}})

@app.route('/', methods=['POST', 'OPTIONS'])
def detect():
    if request.method == 'OPTIONS':
        return '', 204  
    print("Received POST request to /")
    try:
        if not request.is_json:
            print("Error: Request is not JSON")
            return jsonify({"error": "Request must be JSON"}), 400
        user_input = request.json.get('text')
        print(f"User input: {user_input[:50]}")
        if not user_input or not isinstance(user_input, str):
            print("Error: No valid text provided")
            return jsonify({"error": "No valid text provided"}), 400
        
        print("Fetching live news...")
        live_news = scrape_news()
        print(f"Live news sample: {live_news[:2]}")
        if not live_news or all(not news.strip() for news in live_news):
            print("Error: Failed to fetch live news")
            return jsonify({"error": "Failed to fetch live news"}), 500
        
        print("Detecting fake news...")
        result = detect_fake_news(user_input, live_news)
        print(f"Detection result: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)