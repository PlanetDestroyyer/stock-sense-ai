document.addEventListener('DOMContentLoaded', function() {
    const voiceBtn = document.getElementById('voice-btn');
    const voiceStatus = document.getElementById('voice-status');
    const chatInput = document.getElementById('chat-input');
    const clearChatBtn = document.getElementById('clear-chat');
    
    // Check if browser supports speech recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;
    
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            voiceBtn.classList.add('active');
            voiceStatus.classList.add('active');
        };
        
        recognition.onend = function() {
            voiceBtn.classList.remove('active');
            voiceStatus.classList.remove('active');
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            chatInput.value = transcript;
            sendMessage();
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error', event.error);
            voiceBtn.classList.remove('active');
            voiceStatus.classList.remove('active');
            addAIMessage("Sorry, I couldn't understand your voice command. Please try again.");
        };
        
        voiceBtn.addEventListener('click', function() {
            if (voiceBtn.classList.contains('active')) {
                recognition.stop();
            } else {
                try {
                    recognition.start();
                } catch (e) {
                    console.error('Speech recognition failed:', e);
                    addAIMessage("Voice recognition is not available. Please check your microphone settings.");
                }
            }
        });
    } else {
        voiceBtn.style.display = 'none';
        addAIMessage("Your browser doesn't support speech recognition. Try Chrome or Edge.");
    }
    
    // Clear chat functionality
    clearChatBtn.addEventListener('click', function() {
        document.getElementById('chat-messages').innerHTML = `
            <div class="chat-message ai-message">
                <p>Hello! I'm your AI stock assistant. How can I help you today?</p>
            </div>
        `;
    });
    
    function addAIMessage(message) {
        const aiMsg = document.createElement('div');
        aiMsg.className = 'chat-message ai-message';
        aiMsg.innerHTML = `<p>${message}</p>`;
        document.getElementById('chat-messages').appendChild(aiMsg);
        document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
    }
});