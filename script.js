const chatBox = document.getElementById("chat-box");

const userInput = document.getElementById("user-input");

const typingArea = document.getElementById("typing-area");

const sendBtn = document.getElementById("send-btn");


// SEND MESSAGE
async function sendMessage() {

    const message = userInput.value.trim();

    // Prevent empty messages
    if (message === "") return;

    // Disable button while thinking
    sendBtn.disabled = true;

    // Add user message
    addMessage(message, "user-message");

    // Clear input
    userInput.value = "";

    // Show typing animation
    showTyping();

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

        // If server fails
        if (!response.ok) {
            throw new Error("Server failed");
        }

        const data = await response.json();

        // Simulate realistic AI delay
        setTimeout(() => {

            hideTyping();

            addMessage(data.reply, "bot-message");

            sendBtn.disabled = false;

        }, 1000);

    }

    catch (error) {

        hideTyping();

        addMessage(
            "⚠️ Connection to Abgrade failed.",
            "bot-message"
        );

        sendBtn.disabled = false;
    }
}


// ADD MESSAGE
function addMessage(text, className) {

    const messageDiv = document.createElement("div");

    messageDiv.className = `message ${className}`;

    // Smooth typing-like rendering
    typeText(messageDiv, text);

    chatBox.appendChild(messageDiv);

    scrollToBottom();
}


// TYPE EFFECT
function typeText(element, text) {

    let index = 0;

    const speed = 18;

    function type() {

        if (index < text.length) {

            element.innerHTML += text.charAt(index);

            index++;

            scrollToBottom();

            setTimeout(type, speed);

        }
    }

    type();
}


// SHOW TYPING
function showTyping() {

    typingArea.classList.remove("hidden");

    scrollToBottom();
}


// HIDE TYPING
function hideTyping() {

    typingArea.classList.add("hidden");
}


// AUTO SCROLL
function scrollToBottom() {

    chatBox.scrollTop = chatBox.scrollHeight;
}


// ENTER KEY SEND
userInput.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {

        sendMessage();
    }
});


// INPUT FOCUS EFFECT
userInput.addEventListener("focus", () => {

    userInput.placeholder = "Ask anything...";
});


userInput.addEventListener("blur", () => {

    userInput.placeholder = "Message Abgrade...";
});