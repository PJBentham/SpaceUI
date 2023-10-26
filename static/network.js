export const socket = io.connect('http://127.0.0.1:5000');

export function initializeSocketListeners() {
    // Call this function once to avoid adding multiple event listeners
    console.log("Initializing socket.io event listeners...");
    // Socket for receiving messages
    socket.on('receive_message', function(data) {
        speak(data.message);
        let chatBox = document.getElementById("chatBox");
        // Remove typing animation if it exists
        let typingDiv = chatBox.querySelector(".chat-typing");
        if (typingDiv) chatBox.removeChild(typingDiv);
        // Create and display computer response element
        let responseDiv = document.createElement("div");
        responseDiv.classList.add("chat-response");
        responseDiv.innerHTML = "<strong>Computer:</strong> " + data.message;
        chatBox.appendChild(responseDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // auto scroll to bottom after computer's response is added
    });
    // Socket for receiving speed
    socket.on('request_speed', function() {
        let speedValueSpan = document.getElementById("speedValue");
        let speedValue = speedValueSpan.textContent;
        socket.emit('send_speed', { speed: speedValue });
    });
    // Socket for Captain's Log
    const logForm = document.getElementById('logForm');
    if (logForm) {
        logForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting the traditional way
            const logTitle = logForm.querySelector('input[name="log_title"]').value;
            const logContent = logForm.querySelector('textarea[name="log_content"]').value;
            socket.emit('submit_log', { log_title: logTitle, log_content: logContent });
        });
    }
    socket.on('log_status', function(data) {
        if (data.status === 'success') {
            console.log('Log submitted successfully!');
        } else {
            console.log('Failed to submit log.');
        }
    });
    socket.on('update_logs', function() {
        const logContainer = document.getElementById('logContainer');
        if (logContainer) {
            fetch('/get_logs')
                .then(response => response.text())
                .then(html => {
                    logContainer.innerHTML = html;
                    logContainer.scrollTop = logContainer.scrollHeight;
                })
                .catch(error => console.error('Error fetching logs:', error));
        }
    });
}