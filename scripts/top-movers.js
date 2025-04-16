document.addEventListener('DOMContentLoaded', function() {
    // Time filter for top movers
    document.querySelectorAll('#movers-section .time-filter button').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelector('#movers-section .time-filter button.active').classList.remove('active');
            this.classList.add('active');
            updateMoversData(this.dataset.time);
        });
    });
    
    function updateMoversData(timeFrame) {
        // In a real app, this would fetch data from an API
        console.log(`Updating movers data for ${timeFrame}`);
        
        // Simulate data changes
        const stocks = {
            gainers: [
                { id: 'nvda-mover-card', baseChange: 5.32 },
                { id: 'aapl-mover-card', baseChange: 3.78 },
                { id: 'msft-mover-card', baseChange: 2.91 }
            ],
            losers: [
                { id: 'tsla-mover-card', baseChange: -4.56 },
                { id: 'amzn-mover-card', baseChange: -2.89 },
                { id: 'intc-mover-card', baseChange: -1.95 }
            ]
        };
        
        // Update gainers
        stocks.gainers.forEach(stock => {
            const card = document.getElementById(stock.id);
            const changeElement = card.querySelector('span');
            const volumeElement = card.querySelector('small');
            
            // Simulate different changes based on time frame
            let newChange, newVolume;
            if (timeFrame === 'today') {
                newChange = stock.baseChange;
                newVolume = Math.round(Math.random() * 50) + 'M';
            } else if (timeFrame === 'week') {
                newChange = stock.baseChange * (1 + Math.random() * 0.5);
                newVolume = Math.round(Math.random() * 100) + 'M';
            } else {
                newChange = stock.baseChange * (1 + Math.random());
                newVolume = Math.round(Math.random() * 200) + 'M';
            }
            
            changeElement.textContent = (newChange > 0 ? '+' : '') + newChange.toFixed(2) + '%';
            volumeElement.textContent = 'Volume: ' + newVolume;
        });
        
        // Update losers
        stocks.losers.forEach(stock => {
            const card = document.getElementById(stock.id);
            const changeElement = card.querySelector('span');
            const volumeElement = card.querySelector('small');
            
            // Simulate different changes based on time frame
            let newChange, newVolume;
            if (timeFrame === 'today') {
                newChange = stock.baseChange;
                newVolume = Math.round(Math.random() * 50) + 'M';
            } else if (timeFrame === 'week') {
                newChange = stock.baseChange * (1 + Math.random() * 0.5);
                newVolume = Math.round(Math.random() * 100) + 'M';
            } else {
                newChange = stock.baseChange * (1 + Math.random());
                newVolume = Math.round(Math.random() * 200) + 'M';
            }
            
            changeElement.textContent = (newChange > 0 ? '+' : '') + newChange.toFixed(2) + '%';
            volumeElement.textContent = 'Volume: ' + newVolume;
        });
    }
});