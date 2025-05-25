import React, { useState } from 'react';
import NewsForm from './components/NewsForm';
import ResultsDisplay from './components/ResultsDisplay';
import './components.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (text) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(process.env.REACT_APP_API_URL || 'https://your-factualize.onrender.com/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to analyze news');
      }

      const data = await response.json();
      console.log("Backend response:", data);
      setResults({
        isFake: data.is_fake,
        confidence: data.confidence,
        similarity: data.similarity,
        summary: data.summary
      });
    } catch (err) {
      setError(err.message);
      setResults(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`app-wrapper ${results ? (results.isFake ? 'bg-fake' : 'bg-real') : ''}`}>
      <header>
        <h1 style={{ fontSize: '48px', fontStyle: 'italic', fontWeight: '600', color: '#333' }}>
          <span style={{ color: '#0066cc', fontSize: '52px', marginRight: '12px' }}>📰</span>
          Factualize 🔍
        </h1>
        <h2>Fake News Detector</h2>
        <p style={{ fontSize: '1.1rem', color: '#666' }}>Uncover the truth in seconds! 🚀</p>
      </header>
      {error && <div className="error-message">{error}</div>}
      <NewsForm onSubmit={handleSubmit} loading={loading} />
      <ResultsDisplay results={results} loading={loading} />
    </div>
  );
}

export default App;