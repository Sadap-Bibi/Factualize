import React, { useState } from 'react';

const NewsForm = ({ onSubmit, loading }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim()) {
      alert('Please enter some text to analyze.');
      return;
    }
    onSubmit(text);
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="📰 Paste a news headline or text..."
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? '🔍 Analyzing...' : '🔎 Detect Fake News'}
      </button>
    </form>
  );
};

export default NewsForm;