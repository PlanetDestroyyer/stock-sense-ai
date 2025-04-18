document.addEventListener('DOMContentLoaded', async function () {
    const ctx = document.getElementById('marketChart').getContext('2d');

    async function fetchMarketData(interval = '5m') {
        const res = await fetch(`http://127.0.0.1:5000/api/market-data?interval=${interval}`);
        return await res.json();
    }

    const initialData = await fetchMarketData();

    const marketChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: initialData.labels,
            datasets: [{
                label: 'S&P 500',
                data: initialData.data,
                borderColor: '#6e45e2',
                backgroundColor: 'rgba(110, 69, 226, 0.1)',
                borderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: 'rgba(255,255,255,0.7)' }
                },
                y: {
                    grid: { color: 'rgba(255,255,255,0.1)' },
                    ticks: { color: 'rgba(255,255,255,0.7)' }
                }
            }
        }
    });

    // Update every 30 seconds
    setInterval(async () => {
        const updatedData = await fetchMarketData();
        marketChart.data.labels = updatedData.labels;
        marketChart.data.datasets[0].data = updatedData.data;
        marketChart.update();
    }, 30000);

    // Time range buttons
    document.querySelectorAll('.time-filter button').forEach(button => {
        button.addEventListener('click', async () => {
            document.querySelectorAll('.time-filter button').forEach(b => b.classList.remove('active'));
            button.classList.add('active');
            const interval = button.getAttribute('data-time');
            const newData = await fetchMarketData(interval);
            marketChart.data.labels = newData.labels;
            marketChart.data.datasets[0].data = newData.data;
            marketChart.update();
        });
    });
});
