// Function to show custom alerts
function showAlert(message) {
    const alertBox = document.createElement("div");
    alertBox.className = "custom-alert";
    alertBox.textContent = message;
    document.body.appendChild(alertBox);
    setTimeout(() => alertBox.remove(), 3000);
}

// Function to start listening for voice commands
function startListening() {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onresult = function (event) {
            const command = event.results[0][0].transcript.toLowerCase();
            console.log("Command received: " + command);

            if (command.includes("detect object")) {
                window.location.href = "object.html";
            } else if (command.includes("outdoor navigation")) {
                window.location.href = "map.html";
            } else if (command.includes("indoor navigation")) {
                window.location.href = "indoormap.html";
            }else if (command.includes("describe object")) {
                window.location.href = "describe.html"; // Redirect to user.html
            }
            else if (command.includes("money")) {
                window.location.href = "money.html"; // Redirect to user.html
            } else {
                showAlert("Command not recognized. Please try again!");
            }
        };

        recognition.onerror = function (event) {
            showAlert("Error occurred: " + event.error);
        };

        recognition.start();
    } else {
        showAlert("Speech recognition is not supported in this browser.");
    }
}
// Register Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
            .then((registration) => console.log('Service Worker registered with scope:', registration.scope))
            .catch((error) => console.log('Service Worker registration failed:', error));
    });
}

