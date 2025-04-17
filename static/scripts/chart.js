document.addEventListener('DOMContentLoaded', function() {
    // Initialize Market Chart
    const ctx = document.getElementById('marketChart').getContext('2d');
    const marketChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 20}, (_, i) => {
                const d = new Date();
                d.setMinutes(d.getMinutes() - 20 + i);
                return d.getHours() + ':' + String(d.getMinutes()).padStart(2, '0');
            }),
            datasets: [{
                label: 'S&P 500',
                data: Array.from({length: 20}, () => 4400 + Math.random() * 200),
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
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: 'rgba(255,255,255,0.7)'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255,255,255,0.1)'
                    },
                    ticks: {
                        color: 'rgba(255,255,255,0.7)'
                    }
                }
            }
        }
    });

    // Update chart data periodically
    setInterval(() => {
        marketChart.data.labels.shift();
        const d = new Date();
        marketChart.data.labels.push(d.getHours() + ':' + String(d.getMinutes()).padStart(2, '0'));
        
        marketChart.data.datasets.forEach(dataset => {
            dataset.data.shift();
            const lastValue = dataset.data[dataset.data.length - 1];
            dataset.data.push(lastValue + (Math.random() - 0.5) * 10);
        });
        
        marketChart.update();
    }, 5000);
});