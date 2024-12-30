function addMessage(message, isUser) {
    const messagesDiv = document.getElementById("chat-messages");
    const messageDiv = document.createElement("div");
    messageDiv.className = `flex ${isUser ? "justify-end" : "justify-start"}`;

    const bubble = document.createElement("div");
    bubble.className = `max-w-[70%] rounded-lg px-4 py-2 ${
        isUser ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-800"
    }`;
    bubble.textContent = message;

    messageDiv.appendChild(bubble);
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();

    if (message) {
        addMessage(message, true);
        input.value = "";

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message }),
        })
            .then((response) => response.json())
            .then((data) => {
                addMessage(data.response, false);
            })
            .catch((error) => {
                console.error("Error:", error);
                addMessage("Sorry, I encountered an error. Please try again.", false);
            });
    }
}

const minimizeButton = document.getElementById("minimize-chat");
const chatBody = document.getElementById("chat-body");

minimizeButton.addEventListener("click", () => {
    chatBody.classList.toggle("hidden");
    minimizeButton.querySelector("svg").classList.toggle("rotate-180");
});

document.getElementById("send-button").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});
