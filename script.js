const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");

async function sendMessage() {

    const message = userInput.value.trim();

    if (message === "") return;

    addMessage(message, "user-message");

    userInput.value = "";

    // Typing animation
    const typingDiv = document.createElement("div");
    typingDiv.className = "message bot-message";
    typingDiv.id = "typing";
    typingDiv.innerText = "Abgrade is typing...";
    chatBox.appendChild(typingDiv);

    scrollToBottom();

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        document.getElementById("typing").remove();

        addMessage(data.reply, "bot-message");

    } catch (error) {

        document.getElementById("typing").remove();

        addMessage("Server error.", "bot-message");
    }
}

function addMessage(text, className) {

    const messageDiv = document.createElement("div");

    messageDiv.className = `message ${className}`;

    messageDiv.innerText = text;

    chatBox.appendChild(messageDiv);

    scrollToBottom();
}

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send on Enter
userInput.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }
});