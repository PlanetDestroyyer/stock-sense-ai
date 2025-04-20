
document.addEventListener('DOMContentLoaded', () => {
    const stockDB = [
        { symbol: 'AAPL', name: 'Apple Inc.', logo: 'https://logo.clearbit.com/apple.com' },
        { symbol: 'MSFT', name: 'Microsoft Corp.', logo: 'https://logo.clearbit.com/microsoft.com' },
        { symbol: 'GOOGL', name: 'Alphabet Inc.', logo: 'https://logo.clearbit.com/google.com' },
        { symbol: 'AMZN', name: 'Amazon.com Inc.', logo: 'https://logo.clearbit.com/amazon.com' },
        { symbol: 'NVDA', name: 'NVIDIA Corp.', logo: 'https://logo.clearbit.com/nvidia.com' },
        { symbol: 'TSLA', name: 'Tesla Inc.', logo: 'https://logo.clearbit.com/tesla.com' }
    ];

    function setupAutocomplete(inputId, suggestionBoxId, side) {
        const input = document.getElementById(inputId);
        const suggestionBox = document.getElementById(suggestionBoxId);

        input.addEventListener('input', () => {
            const value = input.value.trim().toUpperCase();
            suggestionBox.innerHTML = '';

            if (value.length === 0) return;

            const matches = stockDB.filter(stock =>
                stock.symbol.toUpperCase().startsWith(value) ||
                stock.name.toUpperCase().includes(value)
            );

            matches.forEach(stock => {
                const item = document.createElement('div');
                item.className = 'suggestion-item';
                item.innerHTML = `
                    <img src="${stock.logo}" alt="${stock.symbol}" width="20" height="20" style="vertical-align: middle;">
                    <span>${stock.symbol} - ${stock.name}</span>
                `;
                item.addEventListener('click', () => {
                    input.value = stock.symbol;
                    suggestionBox.innerHTML = '';
                    fetchAndDisplayStockData(stock.symbol, side);
                });
                suggestionBox.appendChild(item);
            });
        });

        document.addEventListener('click', (event) => {
            if (!suggestionBox.contains(event.target) && event.target !== input) {
                suggestionBox.innerHTML = '';
            }
        });
    }

    function fetchAndDisplayStockData(symbol, side) {
        // 🚀 Replace this with your API call or data fetch logic
        console.log(`Fetch and display data for ${symbol} on ${side} side`);

        // Example: update UI elements based on the `side` (left or right)
        const nameEl = document.getElementById(`${side}-name`);
        const logoEl = document.getElementById(`${side}-logo`);

        const stockInfo = stockDB.find(s => s.symbol === symbol);
        if (stockInfo) {
            nameEl.textContent = stockInfo.name;
            logoEl.src = stockInfo.logo;
        }
    }

    setupAutocomplete('left-symbol', 'left-suggestions', 'left');
    setupAutocomplete('right-symbol', 'right-suggestions', 'right');
});

