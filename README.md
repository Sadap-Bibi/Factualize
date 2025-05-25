# 📰 Factualize - Fake News Detector

**Factualize** is a web application that detects fake news by analyzing user-submitted headlines or text. It compares the input with trusted sources like **The Hindu**, **BBC**, and **Times of India** to determine credibility, confidence level, similarity, and the closest matching headline.

---

## 🔍 Features

- **Analyzes Input**: Evaluates the credibility of submitted news headlines or content.
- **Compares with Live News**: Scrapes headlines from trusted sources for similarity analysis.
- **Delivers Insights**: Returns a fake/real verdict, confidence score, similarity chart, and closest headline.
- **Engaging UI**: Vibrant design with gradients, animations, emojis (📰🔍✅), and responsive layout.

---

## ⚙️ How It Works

### Backend

- **Scraping**: Fetches live headlines from The Hindu, BBC, and Times of India using `requests` and `BeautifulSoup4`.
- **Text Preprocessing**: Uses `NLTK` for tokenization and stopword removal.
- **Similarity Computation**: Applies `TF-IDF` and cosine similarity with `Scikit-learn`.
- **Result Generation**: Predicts authenticity based on comparison with live news sources.

### Frontend

- **User Input**: React form to collect headline/text.
- **API Communication**: Sends data to Flask backend and receives results.
- **Visualization**: Renders verdict, confidence bar, and pie chart using `Chart.js`.

---

## 🧰 Tech Stack

### Backend
- Python 3.8+
- Flask
- NLTK
- Scikit-learn
- Requests & BeautifulSoup4
- Flask-CORS

### Frontend
- React (JavaScript ES6+)
- Chart.js & react-chartjs-2
- HTML5, CSS3 (with gradients and animations)

---

## 🛠 Installation

### Prerequisites
- Python 3.8+
- Node.js
- `virtualenv`

  
## Usage
-Open the app at http://localhost:3000.
-Enter a news headline or text in the form.
-Click "🔎 Detect Fake News".
-View results: fake/real verdict, confidence score, similarity chart, and closest headline from The Hindu, BBC, or Times of India.


## Why Factualize Stands Out
-Trusted Sources: Uses The Hindu, BBC, and Times of India for real-time comparison.
-Lively UI: Combines emojis, animations, and vibrant visuals for engagement.
-Accurate Detection: Leverages NLP and similarity metrics for reliable results.
