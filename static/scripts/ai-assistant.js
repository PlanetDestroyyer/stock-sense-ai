document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const voiceBtn = document.getElementById('voice-btn');
    const voiceStatus = document.getElementById('voice-status');
    const clearChatBtn = document.getElementById('clear-chat');
    
    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'chat-message ai-message loading-container';
        loadingDiv.id = 'loading-container';
        
        loadingDiv.innerHTML = `
            <div class="analyzing-text">
                <span>Analyzing</span>
                <span class="ellipsis"></span>
            </div>
        `;
        
        chatMessages.appendChild(loadingDiv);
        
        // Start the ellipsis animation
        let dotsCount = 0;
        const ellipsisElement = loadingDiv.querySelector('.ellipsis');
        
        window.loadingInterval = setInterval(() => {
            dotsCount = (dotsCount + 1) % 4;
            ellipsisElement.textContent = '.'.repeat(dotsCount);
        }, 500);
        
        scrollToBottom();
    }
    
    function removeLoading() {
        const loadingContainer = document.getElementById('loading-container');
        if (loadingContainer) {
            // Clear the interval to stop the animation
            if (window.loadingInterval) {
                clearInterval(window.loadingInterval);
                window.loadingInterval = null;
            }
            loadingContainer.remove();
        }
    }
    

    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const query = chatInput.value.trim();
        if (!query) return;
        
        // Add user message to chat
        addMessage('user', query);
        chatInput.value = '';
        
        // Show loading indicator
        showLoading();
        
        // Send request to server
        fetch('/ai_assistant', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading indicator
            removeLoading();
            
            if (data.error) {
                addMessage('ai', `Error: ${data.error}`);
                return;
            }
            
            // Process AI response
            const responseData = data.response;
            const message = responseData.response;
            
            // Add AI message to chat
            addMessage('ai', message);
            
            // Add action buttons if stocks are mentioned
            if (responseData.tools_used && responseData.tools_used.length > 0) {
                addActionButtons(responseData);
            }
            
            // Scroll to bottom
            scrollToBottom();
        })
        .catch(error => {
            removeLoading();
            addMessage('ai', `Sorry, there was an error processing your request. Please try again.`);
            console.error('Error:', error);
        });
    });
    
    // Clear chat button
    clearChatBtn.addEventListener('click', function() {
        chatMessages.innerHTML = `
            <div class="chat-message ai-message">
                <p>Hello! I'm your AI stock assistant. How can I help you today?</p>
            </div>
        `;
    });
    
    // Voice input button 
    let recognition = null;
    
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            voiceStatus.style.display = 'block';
            voiceBtn.classList.add('active');
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            chatInput.value = transcript;
        };
        
        recognition.onend = function() {
            voiceStatus.style.display = 'none';
            voiceBtn.classList.remove('active');
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            voiceStatus.style.display = 'none';
            voiceBtn.classList.remove('active');
        };
        
        voiceBtn.addEventListener('click', function() {
            if (voiceBtn.classList.contains('active')) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });
    } else {
        voiceBtn.style.display = 'none';
    }
    
    // Helper Functions
    function addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}-message`;
        
        // Format content with Markdown-like styling
        let formattedContent = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold
            .replace(/\*(.*?)\*/g, '<em>$1</em>')  // Italic
            .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')  // Code blocks
            .replace(/`([^`]+)`/g, '<code>$1</code>')  // Inline code
            .replace(/\n/g, '<br>');  // Line breaks
        
        messageDiv.innerHTML = `<p>${formattedContent}</p>`;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function addActionButtons(responseData) {
        const lastMessage = chatMessages.lastElementChild;
        
        // Check if buttons container already exists
        let buttonsContainer = lastMessage.querySelector('.action-buttons');
        if (!buttonsContainer) {
            buttonsContainer = document.createElement('div');
            buttonsContainer.className = 'action-buttons';
            lastMessage.appendChild(buttonsContainer);
        }
        
        // Add ticker chart button if stock data was used
        if (responseData.tools_used.includes('stock_data') || 
            responseData.tools_used.includes('ticker_info')) {
            
            // Extract potential ticker symbols from the response
            const tickerRegex = /\$([A-Z]{1,5})\b/g;
            const tickerMatches = [...responseData.response.matchAll(tickerRegex)];
            const tickers = tickerMatches.map(match => match[1]);
            
            // Add chart button for each unique ticker
            new Set(tickers).forEach(ticker => {
                const chartBtn = document.createElement('button');
                chartBtn.className = 'action-btn chart-btn';
                chartBtn.innerHTML = `<i class="fas fa-chart-line"></i> ${ticker} Chart`;
                chartBtn.addEventListener('click', function() {
                    window.open(`/comparison?ticker1=${ticker}`, '_blank');
                });
                buttonsContainer.appendChild(chartBtn);
            });
        }
        
        // Add news button if news data was used
        if (responseData.tools_used.includes('yahoo_finance') || 
            responseData.tools_used.includes('news_api')) {
            
            // Extract potential ticker symbols from the response
            const tickerRegex = /\$([A-Z]{1,5})\b/g;
            const tickerMatches = [...responseData.response.matchAll(tickerRegex)];
            const tickers = tickerMatches.map(match => match[1]);
            
            // Add news button for each unique ticker
            new Set(tickers).forEach(ticker => {
                const newsBtn = document.createElement('button');
                newsBtn.className = 'action-btn news-btn';
                newsBtn.innerHTML = `<i class="fas fa-newspaper"></i> ${ticker} News`;
                newsBtn.addEventListener('click', function() {
                    window.open(`/news?query=${ticker}`, '_blank');
                });
                buttonsContainer.appendChild(newsBtn);
            });
        }
    }
    
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});