document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const voiceBtn = document.getElementById('voice-btn');
    const voiceStatus = document.getElementById('voice-status');
    const clearChatBtn = document.getElementById('clear-chat');
    
    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message
        addMessage('user', message);
        
        // Clear input
        chatInput.value = '';
        
        // Show loading indicator
        showLoading();
        
        // Send request to the backend API
        fetch('/ai_assistant', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message }),
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
            let aiMessage = responseData.response;
            
            // Add AI message to chat
            addMessage('ai', aiMessage);
            
            // Add action buttons based on tools used
            if (responseData.tools_used && responseData.tools_used.length > 0) {
                addActionButtons(responseData);
            }
            
            // Scroll to bottom
            scrollToBottom();
        })
        .catch(error => {
            // Remove loading indicator
            removeLoading();
            
            // Show error message
            addMessage('ai', 'Sorry, there was an error processing your request. Please try again.');
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
    
    // Voice input button functionality
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
    
    // Helper functions
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
        
        return messageDiv;
    }
    
    function addActionButtons(responseData) {
        const lastMessage = chatMessages.lastElementChild;
        
        // Create buttons container if it doesn't exist
        let buttonsContainer = lastMessage.querySelector('.action-buttons');
        if (!buttonsContainer) {
            buttonsContainer = document.createElement('div');
            buttonsContainer.className = 'action-buttons';
            lastMessage.appendChild(buttonsContainer);
        }
        
        // Detect stock tickers in the response
        const tickerRegex = /\$?([A-Z]{1,5})\b/g;
        const tickerMatches = [...responseData.response.matchAll(tickerRegex)];
        const tickers = tickerMatches
            .map(match => match[1])
            .filter(ticker => {
                // Filter out common words that might be mistaken for tickers
                const commonWords = ['A', 'I', 'FOR', 'AT', 'BE', 'AI', 'OR', 'IT', 'ON', 'BY'];
                return !commonWords.includes(ticker);
            });
        
        // Add chart buttons for each ticker
        if (tickers.length > 0 || responseData.tools_used.includes('stock_data') || 
            responseData.tools_used.includes('ticker_info')) {
            
            // Use detected tickers or tools_used information
            const tickersToUse = tickers.length > 0 ? [...new Set(tickers)] : ['MSFT']; // Default if no tickers found
            
            tickersToUse.forEach(ticker => {
                const chartBtn = document.createElement('button');
                chartBtn.className = 'action-btn chart-btn';
                chartBtn.innerHTML = `<i class="fas fa-chart-line"></i> ${ticker} Chart`;
                chartBtn.addEventListener('click', function() {
                    window.open(`/comparison?ticker1=${ticker}`, '_blank');
                });
                buttonsContainer.appendChild(chartBtn);
                
                // Also add a news button for this ticker
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
    
    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading-indicator';
        loadingDiv.innerHTML = `
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        `;
        loadingDiv.id = 'loading-indicator';
        chatMessages.appendChild(loadingDiv);
        scrollToBottom();
    }
    
    function removeLoading() {
        const loadingDiv = document.getElementById('loading-indicator');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});