let chartInstance = null;

document.getElementById('newsForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('newsInput').value.trim();
    if (!text) {
        alert('Please enter some text to analyze.');
        return;
    }

    try {
        console.log("Sending POST request to http://127.0.0.1:5000/");
        const response = await fetch('http://127.0.0.1:5000/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server returned ${response.status}: ${errorText}`);
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert(`Failed to fetch results: ${error.message}`);
    }
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const isFakeEl = document.getElementById('isFake');
    const statusIcon = document.getElementById('statusIcon');
    const confidenceEl = document.getElementById('confidence');
    const confidenceFill = document.getElementById('confidenceFill');
    const summaryEl = document.getElementById('summary');

    if (!resultsDiv || !isFakeEl || !statusIcon || !confidenceEl || !confidenceFill || !summaryEl) {
        console.error("One or more DOM elements are missing.");
        return;
    }

    resultsDiv.classList.remove('hidden');
    resultsDiv.classList.add('show');

    if (data.is_fake) {
        isFakeEl.textContent = "Likely Fake News";
        statusIcon.textContent = "⚠️";
        isFakeEl.classList.remove('real');
        isFakeEl.classList.add('fake');
        document.body.classList.remove('real-bg');
        document.body.classList.add('fake-bg');
    } else {
        isFakeEl.textContent = "Likely Real News";
        statusIcon.textContent = "✅";
        isFakeEl.classList.remove('fake');
        isFakeEl.classList.add('real');
        document.body.classList.remove('fake-bg');
        document.body.classList.add('real-bg');
    }

    confidenceEl.textContent = `Confidence: ${data.confidence}%`;
    confidenceFill.style.width = `${Math.max(0, Math.min(100, data.confidence))}%`;
    confidenceFill.style.background = data.is_fake 
        ? "linear-gradient(to right, #ff1a1a, #ff6666)" 
        : "linear-gradient(to right, #00cc00, #66ff66)";

    summaryEl.innerHTML = `
        ${!data.is_fake && data.closest_headline ? `Matching Headline: ${data.closest_headline}\n` : "No matching headline found.\n"}
        Top 3 Matches (Heap):\n${data.top_matches_heap.map(m => `${m[1]} (${m[0].toFixed(2)})`).join('\n')}\n
        Top 3 Matches (BST):\n${data.top_matches_bst.map(m => `${m[1]} (${m[0].toFixed(2)})`).join('\n')}\n
        Clustered: ${data.is_clustered ? 'Yes' : 'No'} (Cluster Size: ${data.cluster_size})
    `;

    if (chartInstance) chartInstance.destroy();
    const ctx = document.getElementById('similarityChart').getContext('2d');
    chartInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Confidence', 'Remaining'],
            datasets: [{
                data: [data.confidence, 100 - data.confidence],
                backgroundColor: [data.is_fake ? '#ff1a1a' : '#00cc00', '#b3b3b3'],
                borderWidth: 1,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                title: { display: true, text: 'Confidence Breakdown' }
            }
        }
    });
}