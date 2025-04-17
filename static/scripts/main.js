document.addEventListener('DOMContentLoaded', function() {
    // Time filter buttons
    document.querySelectorAll('.time-filter button').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelector('.time-filter button.active').classList.remove('active');
            this.classList.add('active');
            
            // In a real app, this would update the chart time frame
            alert(`Loading ${this.dataset.time} data...`);
        });
    });

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