import { initiateHyperdrive, emergencyStop, updateSpeed, toggleCommsPanel, toggleCaptainsLog, sendMessage } from './user_interface.js';
import { initializeSocketListeners } from './network.js';
import {  playSliderSound, playSwitchSound, preloadSpeechAPI, setupSpeechRecognition, setupSpeechSynthesis } from './audio.js';
import { windowResized, statusElement } from './utilities.js';
import { startStarfield } from './background.js';

// Immediately call the initialization function
document.addEventListener("DOMContentLoaded", function() {
    initializeSocketListeners();
    preloadSpeechAPI()
    setupSpeechRecognition();
    setupSpeechSynthesis();

    document.getElementById('hyperdriveSound').src = "/static/audio/Lightspeed.mp3";
    document.getElementById('emergencyStopSound').src = "/static/audio/Woah.mp3";
    document.getElementById('sliderSound').src = "/static/audio/Slider.mp3";
    document.getElementById('switchSound').src = "/static/audio/Switch.mp3";    // Update the text and class of the status element

    // Add event listeners to the buttons
    document.getElementById('hyperdriveButton').addEventListener('click', initiateHyperdrive);
    document.getElementById('emergencyStopButton').addEventListener('click', emergencyStop);
    document.getElementById('enginePower').addEventListener('input', updateSpeed);
    document.getElementById('shieldStrength').addEventListener('input', playSliderSound);
    document.getElementById('lightSwitch').addEventListener('change', playSwitchSound);
    document.getElementById('communicationSwitch').addEventListener('change', toggleCommsPanel);
    document.getElementById('captainsLogSwitch').addEventListener('change', toggleCaptainsLog);

    document.getElementById('chatInput').addEventListener('keydown', function(event) {
    if ((event.ctrlKey || event.metaKey) && (event.key === 'Enter' || event.keyCode === 13)) {
      event.preventDefault();
      sendMessage();
    }
    });

    statusElement.textContent = "Online";
    statusElement.classList.remove("text-danger");
    statusElement.classList.add("text-success");
});

