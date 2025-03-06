// Global variable to store the chart instance
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
    const body = document.body;

    // Null checks for critical elements
    if (!resultsDiv || !isFakeEl || !statusIcon || !confidenceEl || !confidenceFill || !summaryEl) {
        console.error("One or more DOM elements are missing:", {
            resultsDiv, isFakeEl, statusIcon, confidenceEl, confidenceFill, summaryEl
        });
        return;
    }

    // Show results with animation
    resultsDiv.classList.remove('hidden');
    resultsDiv.classList.add('show');

    // Apply fake/real styling and emojis
    if (data.is_fake) {
        isFakeEl.textContent = "Likely Fake News";
        statusIcon.textContent = "⚠️";
        console.log("Setting fake icon to:", statusIcon.textContent);
        isFakeEl.classList.remove('real');
        isFakeEl.classList.add('fake');
        body.classList.remove('real-bg');
        body.classList.add('fake-bg');
    } else {
        isFakeEl.textContent = "Likely Real News";
        statusIcon.textContent = "✅";
        console.log("Setting real icon to:", statusIcon.textContent);
        isFakeEl.classList.remove('fake');
        isFakeEl.classList.add('real');
        body.classList.remove('fake-bg');
        body.classList.add('real-bg');
    }

    // Update confidence bar and text
    confidenceEl.textContent = `Confidence: ${data.confidence}%`;
    console.log("Setting confidence fill width to:", `${data.confidence}%`);
    confidenceFill.style.width = `${Math.max(0, Math.min(100, data.confidence))}%`;
    console.log("Confidence fill width set to:", confidenceFill.style.width);
    if (data.is_fake) {
        confidenceFill.style.background = "linear-gradient(to right, #ff1a1a, #ff6666)";
    } else {
        confidenceFill.style.background = "linear-gradient(to right, #00cc00, #66ff66)";
    }

    // Update summary with closest headline if real, or a message if fake
    if (!data.is_fake && data.closest_headline) {
        summaryEl.textContent = `Matching Headline: ${data.closest_headline}`;
    } else {
        summaryEl.textContent = "No matching headline found. This news may be fake.";
    }

    // Destroy previous chart instance if it exists
    if (chartInstance) {
        chartInstance.destroy();
        console.log("Destroyed previous chart instance");
    }

    // Render new similarity chart
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
                legend: {
                    position: 'bottom',
                    labels: {
                        generateLabels: function(chart) {
                            const data = chart.data;
                            return data.labels.map((label, i) => ({
                                text: `${label}: ${data.datasets[0].data[i]}%`,
                                fillStyle: data.datasets[0].backgroundColor[i],
                                font: { size: 12 }
                            }));
                        }
                    }
                },
                title: { display: true, text: 'Confidence Breakdown', font: { size: 14 } }
            }
        }
    });
}