async function fetchData(url) {
  const res = await fetch(url);
  return res.json();
}

function renderConfidenceChart(data) {
  const symbols = data.map(d => d.symbol);
  const confidences = data.map(d => d.confidence);
  const trace = {
    x: symbols,
    y: confidences,
    type: 'bar',
    marker: { color: '#00ffc3' },
    name: 'Confidence'
  };
  Plotly.newPlot('confidenceChart', [trace], { title: '🧠 Trade Confidence by Symbol' });
}

function renderSentimentChart(data) {
  const symbols = Object.keys(data);
  const sentiments = Object.values(data);
  const trace = {
    x: symbols,
    y: sentiments,
    type: 'bar',
    marker: { color: '#ffa600' },
    name: 'Sentiment'
  };
  Plotly.newPlot('sentimentChart', [trace], { title: '📊 Sentiment Scores by Symbol' });
}

function renderTradesChart(data) {
  const symbols = data.map(d => d.symbol);
  const pnl = data.map(d => d.pnl || 0);
  const trace = {
    x: symbols,
    y: pnl,
    type: 'bar',
    marker: { color: '#ff6361' },
    name: 'PnL'
  };
  Plotly.newPlot('tradesChart', [trace], { title: '💹 PnL by Trade (Simulated)' });
}

async function loadDashboard() {
  const decisions = await fetchData('/api/decisions');
  const sentiment = await fetchData('/api/sentiment');
  const trades = await fetchData('/api/trades');

  renderConfidenceChart(decisions.slice(-10));
  renderSentimentChart(sentiment);
  renderTradesChart(trades.slice(-10));
}

loadDashboard();
