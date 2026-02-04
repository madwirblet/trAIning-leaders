(function() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeChat);
    } else {
        initializeChat();
    }

    function initializeChat() {
        const sendBtn = document.getElementById('send-btn');
        const userInput = document.getElementById('user-input');
        const chatMessages = document.getElementById('chat-messages');

        if (!sendBtn || !userInput) {
            console.error('Chat widget elements not found');
            return;
        }

        // Send message on button click
        sendBtn.addEventListener('click', sendMessage);

        // Send message on Enter key
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        async function sendMessage() {
            const question = userInput.value.trim();
            if (!question) return;

            // Add user message to UI
            appendMessage('User', question, chatMessages);
            userInput.value = '';
            userInput.focus();

            try {
                // Call your backend
                const response = await fetch('https://your-api-url.com/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: question })
                });

                if (!response.ok) throw new Error(`API error: ${response.status}`);

                const data = await response.json();
                appendMessage('AI', data.response, chatMessages);
            } catch (error) {
                appendMessage('System', `Error: ${error.message}`, chatMessages);
                console.error('Chat error:', error);
            }
        }
    }

    function appendMessage(sender, text, container) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-message chat-message-${sender.toLowerCase()}`;
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${escapeHtml(text)}`;
        container.appendChild(msgDiv);
        // Auto-scroll to bottom
        container.scrollTop = container.scrollHeight;
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
})()