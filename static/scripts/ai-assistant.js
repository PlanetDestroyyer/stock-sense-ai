document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const voiceBtn = document.getElementById('voice-btn');
    const voiceStatus = document.getElementById('voice-status');
    const clearChatBtn = document.getElementById('clear-chat');
    
    // Helper Functions
    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'chat-message ai-message loading-container';
        loadingDiv.id = 'loading-container';
        
        loadingDiv.innerHTML = `
            <div class="analyzing-text">
                <span>Analyzing</span>
                <div class="loading-dots">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(loadingDiv);
        scrollToBottom();
    }
    
    function removeLoading() {
        const loadingContainer = document.getElementById('loading-container');
        if (loadingContainer) {
            loadingContainer.remove();
        }
    }
    
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
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

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
});