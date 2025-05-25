# Fake News Detector

## Overview
Fake News Detector is a web-based application designed to determine whether a news headline or text is likely fake or real by comparing it to live news headlines from BBC News. By leveraging Natural Language Processing (NLP) and key Data Structures and Algorithms (DSA), the project showcases the power of structured data management and real-time analysis.

## Features
- **Analyzes Input:** Accepts user-provided news text and evaluates its credibility.
- **Compares with Live News:** Scrapes BBC headlines and computes similarity scores.
- **Delivers Insights:** Provides a fake/real verdict, confidence score, top 3 matching headlines, and news clusters.
- **Data Visualization:** Displays results through a confidence bar and a pie chart.

## How It Works
### Backend
- **Scraping:** Retrieves live news headlines from BBC using `Requests` and `BeautifulSoup4`.
- **Text Preprocessing:** Uses `NLTK` to clean and tokenize input text.
- **Similarity Computation:** Applies `Scikit-learn`'s TF-IDF vectorization and cosine similarity.
- **Data Structures:**
  - **BST (Binary Search Tree):** Stores similarity scores and retrieves top 3 matches efficiently.
  - **Heap (Priority Queue):** Tracks top 3 most similar headlines.
  - **Graph with DFS:** Groups similar news articles into clusters.

### Frontend
- **User Input:** Accepts news text and sends it to the backend.
- **API Calls:** Fetches analysis results.
- **Dynamic UI:** Displays results with structured insights and visual charts.

## Tech Stack
### Backend
- **Python 3.8+** - Core language for processing.
- **Flask** - Lightweight framework for API.
- **Flask-CORS** - Handles cross-origin requests.
- **NLTK** - Text preprocessing (tokenization, stopword removal).
- **Scikit-learn** - TF-IDF vectorization and cosine similarity.
- **Requests & BeautifulSoup4** - Web scraping for live news.

### Frontend
- **HTML5, CSS3** - UI structure and styling.
- **JavaScript (ES6+)** - Dynamic interactions and API calls.
- **Chart.js** - Displays confidence scores as pie charts.

## Data Structures & Algorithms
- **Binary Search Tree (BST):** Efficient similarity score retrieval (O(h) insert, O(n) traversal).
- **Graph with DFS:** Detects clusters of similar news articles (O(n²) build, O(V + E) search).
- **Heap (Priority Queue):** Maintains top 3 most relevant headlines (O(n log k), k=3).

## Installation
### Prerequisites
- Python 3.8+
- Node.js (for frontend development)
- Virtualenv (for dependency management)

### Backend Setup
```sh
# Clone the repository
git clone https://github.com/yourusername/FakeNewsDetector.git
cd FakeNewsDetector

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

### Frontend Setup
```sh
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start the frontend
npm start
```

## Usage
1. Open the application in your browser.
2. Enter a news headline or article text.
3. Click the "Analyze" button.
4. View results, including confidence score, top matches, and clusters.

## Why This Project Stands Out
- **DSA Integration:** Combines BST, Graphs, and Heap to enhance accuracy and efficiency.
- **Real-Time Analysis:** Uses live news data for up-to-date results.
- **User-Friendly:** Interactive UI with data visualization for easy interpretation.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

