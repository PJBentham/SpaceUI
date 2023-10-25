let statusElement = document.getElementById("status");

function initiateHyperdrive() {
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

function emergencyStop() {
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

function playSliderSound() {
  document.getElementById("sliderSound").play();
}

function playSwitchSound() {
  document.getElementById("switchSound").play();
}

function updateSpeed() {
  let enginePower = document.getElementById("enginePower").value;
  let speed = enginePower; // Adjust this formula if needed
  document.getElementById("speedValue").innerText = speed;
}

// Starfield
let stars = [];
let engineSpeed = 0;

function setup() {
  let cnv = createCanvas(windowWidth, windowHeight);
  cnv.style('position', 'fixed');
  cnv.style('top', '0');
  cnv.style('left', '0');
  cnv.style('z-index', '-1');
  for (let i = 0; i < 100; i++) {
    stars.push(new Star());
  }

  let enginePowerElem = document.getElementById("enginePower");
  enginePowerElem.addEventListener('input', function() {
    engineSpeed = parseFloat(enginePowerElem.value);
  });
}



function draw() {
    background(0);
    translate(width / 2, height / 2);

    for (let star of stars) {
        star.update();
        star.show();
    }
}

// Star class
class Star {
  constructor() {
    this.x = random(-width, width);
    this.y = random(-height, height);
    this.z = random(width);
    this.pz = this.z;
  }

  update() {
    if (engineSpeed === 0) {
      return; // Exit the update function early if engineSpeed is zero.
    }

    this.pz = this.z;
    this.z -= 4 + engineSpeed * 0.5;
    if (this.z < 1) {
      this.z = width;
      this.x = random(-width, width);
      this.y = random(-height, height);
      this.pz = this.z;
    }
  }

  show() {
    fill(255);
    noStroke();
    let sx = map(this.x / this.z, 0, 1, 0, width);
    let sy = map(this.y / this.z, 0, 1, 0, height);
    let px = map(this.x / this.pz, 0, 1, 0, width);
    let py = map(this.y / this.pz, 0, 1, 0, height);

    stroke(255);
    line(px, py, sx, sy);
  }
}
// End Starfield

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

document.getElementById('chatInput').addEventListener('keydown', function(event) {
  if ((event.ctrlKey || event.metaKey) && (event.key === 'Enter' || event.keyCode === 13)) {
    event.preventDefault();
    sendMessage();
  }
});

// Speech recognition
if (!('webkitSpeechRecognition' in window)) {
  alert("Your browser does not support speech recognition. Try using Chrome.");
} else {
  let recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = 'en-US';

  recognition.onresult = function(event) {
    let transcript = Array.from(event.results)
                          .map(result => result[0])
                          .map(result => result.transcript)
                          .join('');
    document.getElementById("chatInput").value = transcript;
  };

  recognition.onstart = function() {
    document.getElementById("chatInput").placeholder = "Listening...";
  };

  recognition.onend = function() {
    document.getElementById("chatInput").placeholder = "Type a message or use voice...";
    sendMessage();
  };

  window.startListening = function() {
    recognition.start();
  }
}


// Speech synthesis
let msg = new SpeechSynthesisUtterance();  // Create a new speech object once
msg.lang = 'en-GB'                        // Set the language (you can change this based on preference)
msg.rate = 1.1;                              // Set the speech rate
msg.pitch = 1.2;                             // Set the speech pitch

function speakText(text) {
  msg.text = text;                         // Set the text to be spoken
  speechSynthesis.speak(msg);  // Let the browser speak out the text
}
// End speech synthesis

// Function to toggle the communications panel
function toggleCommsPanel() {
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

function toggleCaptainsLog() {
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
function sendMessage() {
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

// Function to initialize socket.io event listeners
function initializeSocketListeners() {
    // Call this function once to avoid adding multiple event listeners
    console.log("Initializing socket.io event listeners...");
    // Socket for receiving messages
    socket.on('receive_message', function(data) {
        speakText(data.message);
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

function preloadSpeechAPI() {
  let warmUpMsg = new SpeechSynthesisUtterance(" ");
  speechSynthesis.speak(warmUpMsg);
}

// Initialize socket.io
const socket = io.connect('http://127.0.0.1:5000'); // or your server URL

// Immediately call the initialization function
document.addEventListener("DOMContentLoaded", function() {
    initializeSocketListeners();
    preloadSpeechAPI()
    document.getElementById('hyperdriveSound').src = "/static/audio/Lightspeed.mp3";
    document.getElementById('emergencyStopSound').src = "/static/audio/Woah.mp3";
    document.getElementById('sliderSound').src = "/static/audio/Slider.mp3";
    document.getElementById('switchSound').src = "/static/audio/Switch.mp3";    // Update the text and class of the status element
    statusElement.textContent = "Online";
    statusElement.classList.remove("text-danger");
    statusElement.classList.add("text-success");
});