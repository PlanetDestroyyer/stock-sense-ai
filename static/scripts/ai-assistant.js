document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');
    const voiceBtn = document.getElementById('voice-btn');
    const clearChatBtn = document.getElementById('clear-chat');
    const voiceStatus = document.getElementById('voice-status');
    
    // Function to add loading indicator
    function addLoadingIndicator() {
        const loadingMessage = document.createElement('div');
        loadingMessage.className = 'chat-message ai-message loading';
        loadingMessage.innerHTML = `
            <div class="loading-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
            <p>Analyzing market data...</p>
        `;
        chatMessages.appendChild(loadingMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return loadingMessage;
    }
    
    // Function to remove loading indicator
    function removeLoadingIndicator(element) {
        if (element && element.parentNode) {
            element.parentNode.removeChild(element);
        }
    }
    
    // Check if all required elements exist
    if (chatForm && chatInput && chatMessages && sendBtn) {
        // Handle form submission
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent page reload
            const query = chatInput.value.trim();
            if (!query) return;
            
            // Add user message
            const userMessage = document.createElement('div');
            userMessage.className = 'chat-message user-message';
            userMessage.innerHTML = `<p>${query}</p>`;
            chatMessages.appendChild(userMessage);
            chatInput.value = ''; // Clear input
            
            // Add loading indicator
            const loadingIndicator = addLoadingIndicator();
            
            // Set the X-Requested-With header to identify as AJAX request
            try {
                // Send POST request to /ai_assistant
                const response = await fetch('/ai_assistant', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: new URLSearchParams({ query }),
                });
                
                // Remove loading indicator
                removeLoadingIndicator(loadingIndicator);
                
                const data = await response.json();
                console.log("Response data:", data); // For debugging
                
                // Add AI message
                const aiMessage = document.createElement('div');
                aiMessage.className = 'chat-message ai-message';
                let messageContent = '';
                
                if (data.error) {
                    messageContent = `<p style="color: red;">Error: ${data.error}</p>`;
                } else if (data.response) {
                    // Handle the response content
                    const responseData = data.response;
                    
                    if (typeof responseData === 'string') {
                        messageContent = `<p>${responseData}</p>`;
                    } else {
                        messageContent = `<p>${responseData.response || 'No response available'}</p>`;
                        
                        if (responseData.summary) {
                            messageContent += `<p><strong>Summary:</strong> ${responseData.summary}</p>`;
                        }
                        
                        if (responseData.links && responseData.links.length) {
                            messageContent += `<p><strong>Links:</strong></p><ul>`;
                            responseData.links.forEach(link => {
                                messageContent += `<li><a href="${link}" target="_blank">${link}</a></li>`;
                            });
                            messageContent += `</ul>`;
                        }
                        
                        if (responseData.tools_used && responseData.tools_used.length) {
                            messageContent += `<p><strong>Tools Used:</strong> ${responseData.tools_used.join(', ')}</p>`;
                        }
                    }
                } else {
                    messageContent = `<p>Sorry, I couldn't process your request at this time.</p>`;
                }
                
                aiMessage.innerHTML = messageContent;
                chatMessages.appendChild(aiMessage);
                
                // Add stock chart button if the query mentions a stock ticker
                const tickerRegex = /\b[A-Za-z]{1,5}\b/g;
                const potentialTickers = query.match(tickerRegex);
                
                if (potentialTickers && !messageContent.includes("Error:")) {
                    // Find words that look like tickers (1-5 letters)
                    const commonWords = ["the", "a", "an", "and", "or", "but", "for", "in", "on", "at", "to", "by", "is", "are", "was", "were"];
                    const tickers = potentialTickers.filter(word => !commonWords.includes(word.toLowerCase()));
                    
                    if (tickers.length > 0) {
                        const actionButtons = document.createElement('div');
                        actionButtons.style.marginTop = '10px';
                        
                        tickers.forEach(ticker => {
                            const chartButton = document.createElement('button');
                            chartButton.className = 'show-chart';
                            chartButton.setAttribute('data-stock', ticker.toUpperCase());
                            chartButton.textContent = `Show ${ticker.toUpperCase()} Chart`;
                            chartButton.style.marginRight = '5px';
                            actionButtons.appendChild(chartButton);
                            
                            const newsButton = document.createElement('button');
                            newsButton.className = 'read-news';
                            newsButton.setAttribute('data-news', ticker.toLowerCase());
                            newsButton.textContent = `${ticker.toUpperCase()} News`;
                            actionButtons.appendChild(newsButton);
                        });
                        
                        aiMessage.appendChild(actionButtons);
                    }
                }
                
                // Scroll to bottom
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
            } catch (error) {
                // Remove loading indicator
                removeLoadingIndicator(loadingIndicator);
                
                const errorMessage = document.createElement('div');
                errorMessage.className = 'chat-message ai-message';
                errorMessage.innerHTML = `<p style="color: red;">Error: Failed to fetch response</p>`;
                chatMessages.appendChild(errorMessage);
                console.error('Error:', error);
            }
        });
    }
    
    // Handle chart and news buttons click events
    chatMessages.addEventListener('click', (e) => {
        if (e.target.classList.contains('show-chart')) {
            const ticker = e.target.getAttribute('data-stock');
            // Implement your chart display logic here
            alert(`Showing chart for ${ticker}`);
        } else if (e.target.classList.contains('read-news')) {
            const ticker = e.target.getAttribute('data-news');
            // Redirect to news page or implement news display logic
            window.location.href = `/news?query=${ticker}`;
        }
    });
    
    // Clear chat button functionality
    if (clearChatBtn) {
        clearChatBtn.addEventListener('click', () => {
            // Remove all user messages
            const userMessages = chatMessages.querySelectorAll('.user-message');
            userMessages.forEach(msg => msg.remove());
            
            // Remove all AI messages except the welcome message
            const aiMessages = chatMessages.querySelectorAll('.ai-message');
            for (let i = 1; i < aiMessages.length; i++) {
                aiMessages[i].remove();
            }
        });
    }
    
    // Voice button functionality (if you want to implement)
    if (voiceBtn && voiceStatus) {
        voiceBtn.addEventListener('click', () => {
            // Implement speech recognition if needed
            alert('Voice recognition feature coming soon!');
        });
    }
});