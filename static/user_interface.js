import { playSliderSound, playSwitchSound } from './audio.js';
import { socket } from './network.js';
// Funtion to initiate the hyperdrive
export function initiateHyperdrive() {
  document.getElementById("hyperdriveSound").play();
  let enginePowerSlider = document.getElementById("enginePower");
  let speedIncreaseInterval = setInterval(function() {
    // Increment the slider value
    enginePowerSlider.value = parseInt(enginePowerSlider.value) + 1;

    updateSpeed();
    // If the slider value has reached its maximum, clear the interval
    if (enginePowerSlider.value >= 100) {
      clearInterval(speedIncreaseInterval);
    }
  }, 50);  // Increase by 1 every 50 milliseconds. Adjust this value for faster/slower speed.

  let originalText = $("#hyperdriveButton").text();
  $("#hyperdriveButton").text("Hyperdrive Activated!")
    .css("box-shadow", "0 0 30px #00f")
    .attr("disabled", "disabled");

  setTimeout(function() {
    $("#hyperdriveButton").text(originalText)
      .css("box-shadow", "0 0 15px #ff0")
      .removeAttr("disabled");
  }, 2000);
}

// Function to update the speed value
export function emergencyStop() {
  document.getElementById("emergencyStopSound").play();
  let enginePowerSlider = document.getElementById("enginePower");
  let speedDecreaseInterval = setInterval(function() {
    // Increment the slider value
    enginePowerSlider.value = parseInt(enginePowerSlider.value) - 4;

    updateSpeed();
    // If the slider value has reached its maximum, clear the interval
    if (enginePowerSlider.value <= 0) {
      clearInterval(speedDecreaseInterval);
    }
  }, 50);  // Increase by 1 every 50 milliseconds. Adjust this value for faster/slower speed.

  let originalText = $("#emergencyStopButton").text();
  $("#emergencyStopButton").text("EMERGENCY STOPPED!")
    .css("box-shadow", "0 0 30px #f00")
    .attr("disabled", "disabled");

  setTimeout(function() {
    $("#emergencyStopButton").text(originalText)
      .css("box-shadow", "0 0 15px #ff0")
      .removeAttr("disabled");
  }, 2000);
}

// Function to update the speed value
export function updateSpeed() {
  let enginePower = document.getElementById("enginePower").value;
  let speed = enginePower; // Adjust this formula if needed
  document.getElementById("speedValue").innerText = speed;
}

// Function to toggle the communications panel
export function toggleCommsPanel() {
    let switchState = document.getElementById("communicationSwitch").checked;
    let panel = document.getElementById("communicationsPanel");

    if (switchState) {
        // If the switch is ON, show the panel
        panel.style.display = "block";
    } else {
        // If the switch is OFF, hide the panel
        panel.style.display = "none";
    }

    playSwitchSound();
}

// Function to toggle the Captain's Log panel
export function toggleCaptainsLog() {
    let switchState = document.getElementById("captainsLogSwitch").checked;
    let panel = document.getElementById("captainsLogPanel");

    if (switchState) {
        // If the switch is ON, show the panel
        panel.style.display = "block";
    } else {
        // If the switch is OFF, hide the panel
        panel.style.display = "none";
    }

    playSwitchSound();
}

// Function to send message to the server
export function sendMessage() {
    let message = document.getElementById("chatInput").value;
    let chatBox = document.getElementById("chatBox");

    if (message.trim() !== "") {
        // Create user message element
        let userMessageDiv = document.createElement("div");
        userMessageDiv.classList.add("chat-message");
        userMessageDiv.innerHTML = "<strong>User:</strong> " + message;
        chatBox.appendChild(userMessageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // auto scroll to bottom after user's message is added
        document.getElementById("chatInput").value = ""; // clear input

        // Display typing animation
        let typingDiv = document.createElement("div");
        typingDiv.classList.add("chat-typing");
        chatBox.appendChild(typingDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // auto scroll to bottom after typing animation is added

        // Send message using socket.io
        socket.emit('send_message', { message: message });
    }
}