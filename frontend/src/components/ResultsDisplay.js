import React from 'react';
import ConfidenceBar from './ConfidenceBar';
import SimilarityChart from './SimilarityChart';

const ResultsDisplay = ({ results, loading }) => {
  if (loading) {
    return (
      <div className="loading">
        <span className="pulse-emoji">🔍</span> Analyzing news...
      </div>
    );
  }

  if (!results) {
    return null;
  }

  const { isFake, confidence, similarity, summary } = results;

  return (
    <div className={`results-container`}>
      <div className={`result-box ${isFake ? 'fake' : 'real'}`}>
        <h2>Analysis Result</h2>
        <p className="verdict">
          This news appears to be <span>{isFake ? 'FAKE 🚫' : 'REAL ✅'}</span>
        </p>
        <ConfidenceBar confidence={confidence} />
        <SimilarityChart similarity={similarity} />
        <div className="matched-headline">
          <h4>Closest Match from Live News:</h4>
          <p>{summary ? summary : 'No matching headline found.'}</p>
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;