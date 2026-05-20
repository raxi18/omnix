document.getElementById('send-btn').addEventListener('click', sendMessage);

// Allow pressing "Enter" on the keyboard to send messages
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const inputElement = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const messageText = inputElement.value.trim();

    // Don't send empty messages
    if (messageText === "") return;

    // 1. Clear input field immediately
    inputElement.value = "";

    // 2. Append User Message to Chat Window
    appendMessage(messageText, 'user-message');

    // 3. Append a temporary typing indicator for Omnix
    const loadingId = appendMessage("Omnix is thinking...", 'bot-message');

    try {
        // 4. Send the message to our Python backend server
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: messageText }),
        });

        const data = await response.json();
        
        // Remove the temporary loading text
        document.getElementById(loadingId).remove();

        // 5. Append the real AI response to the screen
        appendMessage(data.response, 'bot-message');

    } catch (error) {
        console.error("Error:", error);
        document.getElementById(loadingId).remove();
        appendMessage("Sorry, I had trouble connecting to the night sky. Try again.", 'bot-message');
    }
}

// Helper function to dynamically add messages to the UI
function appendMessage(text, className) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    const uniqueId = 'msg-' + Date.now(); // unique ID to track loading state
    
    messageDiv.id = uniqueId;
    messageDiv.className = `message ${className}`;
    messageDiv.innerText = text;
    
    chatBox.appendChild(messageDiv);
    
    // Smoothly scroll the chat box to the very bottom
    chatBox.scrollTop = chatBox.scrollHeight;
    
    return uniqueId;
}
