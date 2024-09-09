document.addEventListener('DOMContentLoaded', function() {
    const currentPrice = parseFloat(document.getElementById('last-value').textContent.split(' ')[0]);
    const previousClose = parseFloat("{{ stock_info.previousClose }}");

    const change = currentPrice - previousClose;
    const changePercent = (change / previousClose * 100).toFixed(2);
    const valueChangeElement = document.getElementById('value-change');

    valueChangeElement.textContent = `${change.toFixed(2)} (${changePercent}%)`;
    valueChangeElement.classList.add(change >= 0 ? 'positive' : 'negative');
});