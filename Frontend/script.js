document.getElementById('newsForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('newsInput').value;
  
    try {
      const response = await fetch('http://127.0.0.1:5000/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const data = await response.json();
      displayResults(data);
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to fetch results. Please check the console for details.');
    }
  });
  
  function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.classList.remove('hidden');
  
    document.getElementById('isFake').textContent =
      data.is_fake ? "This news is likely fake." : "This news is likely real.";
    document.getElementById('confidence').textContent =
      `Confidence: ${data.confidence}%`;
    document.getElementById('summary').textContent =
      `Summary: ${data.summary}`;
  }