(function() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeChat);
    } else {
        initializeChat();
    }

    function initializeChat() {
        console.log('[Chat Widget] Initializing...');
        
        const toggleBtn = document.getElementById('chat-toggle-btn');
        const chatWidget = document.getElementById('ai-chat-widget');
        const closeBtn = document.getElementById('chat-close-btn');
        const sendBtn = document.getElementById('send-btn');
        const userInput = document.getElementById('user-input');
        const chatMessages = document.getElementById('chat-messages');

        console.log('[Chat Widget] Elements found:', {
            toggleBtn: !!toggleBtn,
            chatWidget: !!chatWidget,
            closeBtn: !!closeBtn,
            sendBtn: !!sendBtn,
            userInput: !!userInput,
            chatMessages: !!chatMessages
        });

        if (!toggleBtn || !chatWidget || !closeBtn || !sendBtn || !userInput || !chatMessages) {
            console.error('[Chat Widget] ERROR: Some elements not found!');
            return;
        }

        console.log('[Chat Widget] All elements found successfully');

        // Toggle chat widget
        toggleBtn.addEventListener('click', function(e) {
            console.log('[Chat Widget] Toggle button clicked!');
            e.preventDefault();
            e.stopPropagation();
            
            if (chatWidget.style.display === 'none' || chatWidget.style.display === '') {
                console.log('[Chat Widget] Opening chat...');
                chatWidget.style.display = 'flex';
                toggleBtn.classList.add('hidden');
                userInput.focus();
            }
        });

        console.log('[Chat Widget] Click listener added to toggle button');

        // Close chat widget
        closeBtn.addEventListener('click', function(e) {
            console.log('[Chat Widget] Close button clicked!');
            e.preventDefault();
            e.stopPropagation();
            chatWidget.style.display = 'none';
            toggleBtn.classList.remove('hidden');
        });

        // Send message on button click
        sendBtn.addEventListener('click', sendMessage);

        // Send message on Enter key
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        async function sendMessage() {
            const question = userInput.value.trim();
            if (!question) return;

            // Disable input while processing
            userInput.disabled = true;
            sendBtn.disabled = true;

            // Add user message to UI
            appendMessage('User', question, chatMessages);
            userInput.value = '';

            // Show loading indicator
            const loadingId = showLoading(chatMessages);

            try {
                // Call backend API
                const response = await fetch('https://training-leaders.onrender.com/chat/', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        message: question  // matches backend's expected key
                    })
                });

                // Remove loading indicator
                removeLoading(loadingId, chatMessages);

                if (!response.ok) {
                    throw new Error(`API error: ${response.status}`);
                }

                const data = await response.json();
                
                // Handle different response formats
                const aiResponse = data.message || data.response || data.answer || 'No response received';

                // Add delay to simulate thinking, then show response
                const typingDelay = Math.min(2000, aiResponse.length * 20);
                setTimeout(() => { appendMessage('AI', aiResponse, chatMessages); }, typingDelay);

            } catch (error) {
                // Remove loading indicator
                removeLoading(loadingId, chatMessages);
                
                // Show error message
                appendMessage('System', `Unable to connect to AI service. Please check your API configuration or try again later.`, chatMessages);
                console.error('Chat error:', error);
            } finally {
                // Re-enable input
                userInput.disabled = false;
                sendBtn.disabled = false;
                userInput.focus();
            }
        }

        const AVATAR_URL = "https://raw.githubusercontent.com/madwirblet/trAIning-leaders/refs/heads/main/frontend/Mascot.png";

        function appendMessage(sender, text, container) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `chat-message chat-message-${sender.toLowerCase()}`;

            const content = document.createElement('div');

            // Add sender label for system messages
            if (sender === 'System') {
                const label = document.createElement('strong');
                label.textContent = 'System';
                content.appendChild(label);
            }

            const textNode = document.createTextNode(text);
            content.appendChild(textNode);
            msgDiv.appendChild(content);

            // Wrap AI messages with avatar
            if (sender === 'AI') {
                const wrapper = document.createElement('div');
                wrapper.className = 'chat-message-ai-wrapper';
                const avatar = document.createElement('img');
                avatar.src = AVATAR_URL;
                avatar.className = 'chat-avatar';
                avatar.alt = 'Assistant';
                wrapper.appendChild(avatar);
                wrapper.appendChild(msgDiv);
                container.appendChild(wrapper);
            } else {
                container.appendChild(msgDiv);
            }

            // Auto-scroll to bottom
            container.scrollTop = container.scrollHeight;
        }

        function showLoading(container) {
            const loadingId = 'loading-' + Date.now();
            const wrapper = document.createElement('div');
            wrapper.className = 'chat-message-ai-wrapper';
            wrapper.id = loadingId;
            const avatar = document.createElement('img');
            avatar.src = AVATAR_URL;
            avatar.className = 'chat-avatar';
            avatar.alt = 'Assistant';
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'chat-message chat-message-ai';
            loadingDiv.innerHTML = `<div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>`;
            wrapper.appendChild(avatar);
            wrapper.appendChild(loadingDiv);
            container.appendChild(wrapper);
            container.scrollTop = container.scrollHeight;
            return loadingId;
        }

        function removeLoading(loadingId, container) {
            const loadingDiv = document.getElementById(loadingId);
            if (loadingDiv) {
                loadingDiv.remove();
            }
        }

        // Add welcome message
        setTimeout(function() {
            appendMessage('AI', 'Hello! I\'m your Leadership Course Assistant. Ask me anything about the lecture material! (I\'m still a work in progress!)', chatMessages);
        }, 500);
        const hintBubble = document.getElementById('chat-hint-bubble');

    // Show the bubble after 1.5s
    setTimeout(() => {
        if (hintBubble) hintBubble.classList.add('visible');
    }, 1200);

    // Collapse the pill and hide bubble after 4.5s
    setTimeout(() => {
        const btn = document.getElementById('chat-toggle-btn');
        if (btn) btn.classList.add('collapsed');
        if (hintBubble) hintBubble.classList.remove('visible');
    }, 9000);

    // Cleanup: If they open the chat manually, hide the bubble immediately
    toggleBtn.addEventListener('click', () => {
        if (hintBubble) hintBubble.style.display = 'none';
    });
    }
})()