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

    // Time filter buttons
    document.querySelectorAll('.time-filter button').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelector('.time-filter button.active').classList.remove('active');
            this.classList.add('active');
            
            // In a real app, this would update the chart time frame
            alert(`Loading ${this.dataset.time} data...`);
        });
    });

    // Navigation links
    document.getElementById('dashboard-link').addEventListener('click', function(e) {
        e.preventDefault();
        showSection('dashboard');
    });
    
    document.getElementById('movers-link').addEventListener('click', function(e) {
        e.preventDefault();
        showSection('movers');
    });
    
    document.getElementById('news-link').addEventListener('click', function(e) {
        e.preventDefault();
        showSection('news');
    });
    
    document.getElementById('assistant-link').addEventListener('click', function(e) {
        e.preventDefault();
        showSection('assistant');
    });

    function showSection(section) {
        document.getElementById('dashboard-section').style.display = 'none';
        document.getElementById('news-section').style.display = 'none';
        document.getElementById('assistant-section').style.display = 'none';
        document.getElementById('movers-section').style.display = 'none';
        
        document.querySelector('.sidebar-nav a.active').classList.remove('active');
        
        if (section === 'dashboard') {
            document.getElementById('dashboard-section').style.display = 'block';
            document.getElementById('dashboard-link').classList.add('active');
        } else if (section === 'news') {
            document.getElementById('news-section').style.display = 'block';
            document.getElementById('news-link').classList.add('active');
        } else if (section === 'assistant') {
            document.getElementById('assistant-section').style.display = 'block';
            document.getElementById('assistant-link').classList.add('active');
        } else if (section === 'movers') {
            document.getElementById('movers-section').style.display = 'block';
            document.getElementById('movers-link').classList.add('active');
        }
    }

    // Stock analysis buttons
    document.querySelectorAll('.analyze-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const stock = this.dataset.stock;
            alert(`Analyzing ${stock}... Showing detailed analysis.`);
            // In a real app, this would show a detailed analysis
        });
    });

    // Show chart buttons
    document.querySelectorAll('.show-chart').forEach(btn => {
        btn.addEventListener('click', function() {
            const stock = this.dataset.stock;
            alert(`Showing detailed chart for ${stock}`);
            // In a real app, this would show a detailed chart
        });
    });

    // Read news buttons
    document.querySelectorAll('.read-news').forEach(btn => {
        btn.addEventListener('click', function() {
            const news = this.dataset.news;
            alert(`Showing news: ${news}`);
            // In a real app, this would show the news article
        });
    });

    // AI Chat functionality
    document.getElementById('send-btn').addEventListener('click', sendMessage);
    document.getElementById('chat-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (!message) return;
        
        // Add user message
        const userMsg = document.createElement('div');
        userMsg.className = 'chat-message user-message';
        userMsg.innerHTML = `<p>${message}</p>`;
        document.getElementById('chat-messages').appendChild(userMsg);
        
        // Clear input
        input.value = '';
        
        // Simulate AI response
        setTimeout(() => {
            const aiMsg = document.createElement('div');
            aiMsg.className = 'chat-message ai-message';
            
            if (message.toLowerCase().includes('nvda') || message.toLowerCase().includes('nvidia')) {
                aiMsg.innerHTML = `
                    <p>NVDA is currently up 3.21% due to positive news about their new AI chip. The stock is showing strong momentum with increasing volume.</p>
                    <div style="margin-top:10px;">
                        <button class="show-chart" data-stock="NVDA" style="margin-right:5px;">Show Chart</button>
                        <button class="read-news" data-news="nvidia-ai">Read News</button>
                    </div>
                `;
            } else if (message.toLowerCase().includes('aapl') || message.toLowerCase().includes('apple')) {
                aiMsg.innerHTML = `
                    <p>AAPL is up 2.45% today after announcing new AI features. The RSI is at 62, suggesting there may still be upside potential.</p>
                    <div style="margin-top:10px;">
                        <button class="show-chart" data-stock="AAPL" style="margin-right:5px;">Show Chart</button>
                        <button class="read-news" data-news="apple-ai">Read News</button>
                    </div>
                `;
            } else {
                aiMsg.innerHTML = `
                    <p>I've analyzed your query about "${message}". Based on current market data, this stock appears to be in a consolidation phase.</p>
                    <div style="margin-top:10px;">
                        <button class="show-chart" data-stock="MSFT" style="margin-right:5px;">Show Chart</button>
                        <button class="read-news" data-news="market-trends">Market Trends</button>
                    </div>
                `;
            }
            
            document.getElementById('chat-messages').appendChild(aiMsg);
            
            // Add event listeners to new buttons
            aiMsg.querySelector('.show-chart').addEventListener('click', function() {
                const stock = this.dataset.stock;
                alert(`Showing detailed chart for ${stock}`);
            });
            
            aiMsg.querySelector('.read-news').addEventListener('click', function() {
                const news = this.dataset.news;
                alert(`Showing news: ${news}`);
            });
            
            // Scroll to bottom
            document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
        }, 1000);
    }

    // Simulate stock price changes
    setInterval(() => {
        const stocks = [
            { id: 'aapl-card', symbol: 'AAPL', base: 189.37 },
            { id: 'nvda-card', symbol: 'NVDA', base: 467.65 },
            { id: 'tsla-card', symbol: 'TSLA', base: 260.54 },
            { id: 'aapl-mover-card', symbol: 'AAPL', base: 3.78 },
            { id: 'nvda-mover-card', symbol: 'NVDA', base: 5.32 },
            { id: 'msft-mover-card', symbol: 'MSFT', base: 2.91 },
            { id: 'tsla-mover-card', symbol: 'TSLA', base: -4.56 },
            { id: 'amzn-mover-card', symbol: 'AMZN', base: -2.89 },
            { id: 'intc-mover-card', symbol: 'INTC', base: -1.95 }
        ];
        
        stocks.forEach(stock => {
            const card = document.getElementById(stock.id);
            if (!card) return;
            
            const changeElement = card.querySelector('span');
            if (!changeElement) return;
            
            const currentChange = parseFloat(changeElement.textContent);
            const newChange = currentChange + (Math.random() - 0.5) * 0.3;
            
            changeElement.textContent = (newChange > 0 ? '+' : '') + newChange.toFixed(2) + '%';
            changeElement.className = newChange >= 0 ? 'up' : 'down';
            
            // Flash the card to show update
            card.style.backgroundColor = 'rgba(255,255,255,0.1)';
            setTimeout(() => {
                card.style.backgroundColor = 'rgba(255,255,255,0.05)';
            }, 300);
        });
    }, 3000);
});