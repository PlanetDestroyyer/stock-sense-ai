document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendBtn = document.getElementById('send-btn');
    const clearChatBtn = document.getElementById('clear-chat');
    const voiceBtn = document.getElementById('voice-btn');
    const voiceStatus = document.getElementById('voice-status');

    // Clean output by removing \n, }} etc.
    function cleanOutput(text) {
        return text
            .replace(/\\n/g, ' ')
            .replace(/}}/g, '')
            .replace(/\s{2,}/g, ' ')
            .trim();
    }

    // Add loading indicator
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

    // Remove loading indicator
    function removeLoadingIndicator(loadingElement) {
        if (loadingElement && loadingElement.parentNode) {
            loadingElement.remove();
        }
    }

    // Add message to chat
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${isUser ? 'user-message' : 'ai-message'}`;
        messageDiv.innerHTML = `<p>${content}</p>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return messageDiv;
    }

    // Add formatted AI response
    function addFormattedResponse(responseData) {
        let messageContent = '';

        if (typeof responseData === 'string') {
            messageContent = cleanOutput(responseData);
        } else {
            messageContent = cleanOutput(responseData.response || 'No response available');

            if (responseData.summary) {
                messageContent += `<p><strong>🧠 Summary:</strong> ${cleanOutput(responseData.summary)}</p>`;
            }

            if (responseData.tools_used?.length) {
                messageContent += `<p><strong>🛠 Tools Used:</strong> ${responseData.tools_used.join(', ')}</p>`;
            }

            if (responseData.links?.length) {
                messageContent += '<p><strong>🔗 Related Links:</strong><br>';
                responseData.links.forEach(link => {
                    messageContent += `<a href="${link}" target="_blank">${link}</a><br>`;
                });
                messageContent += '</p>';
            }
        }

        addMessage(messageContent, false);
    }

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = chatInput.value.trim();
        if (!query) return;

        addMessage(query, true);
        chatInput.value = '';

        const loadingIndicator = addLoadingIndicator();

        try {
            const response = await fetch('/ai_assistant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ query })
            });

            if (!response.ok) throw new Error(`Server responded with status ${response.status}`);

            const data = await response.json();
            console.log("API Response:", data);

            removeLoadingIndicator(loadingIndicator);

            if (data.error) {
                addMessage(`❌ Error: ${data.error}`, false);
            } else {
                addFormattedResponse(data.response);
            }
        } catch (error) {
            removeLoadingIndicator(loadingIndicator);
            addMessage(`❌ Error: ${error.message}`, false);
            console.error('Fetch error:', error);
        }
    });

    // Clear chat
    clearChatBtn?.addEventListener('click', () => {
        const messages = chatMessages.querySelectorAll('.chat-message');
        for (let i = 1; i < messages.length; i++) {
            messages[i].remove();
        }
    });

    // Voice button (placeholder)
    voiceBtn?.addEventListener('click', () => {
        voiceStatus.style.display = 'block';
        setTimeout(() => {
            voiceStatus.style.display = 'none';
        }, 2000);
        alert('Voice recognition will be implemented soon!');
    });

    // Auto-focus
    chatInput.focus();
});
