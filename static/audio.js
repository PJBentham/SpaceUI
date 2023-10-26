export function playSliderSound() {
  document.getElementById("sliderSound").play();
}

export function playSwitchSound() {
  document.getElementById("switchSound").play();
}

export function preloadSpeechAPI() {
  let warmUpMsg = new SpeechSynthesisUtterance(" ");
  speechSynthesis.speak(warmUpMsg);
}

export function setupSpeechRecognition() {
  if (!('webkitSpeechRecognition' in window)) {
    alert("Your browser does not support speech recognition. Try using Chrome.");
    return;
  }

  const recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = 'en-US';

  recognition.onresult = function(event) {
    const transcript = Array.from(event.results)
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

export function setupSpeechSynthesis() {
  const msg = new SpeechSynthesisUtterance();
  msg.lang = 'en-GB';
  msg.rate = 1.1;
  msg.pitch = 1.2;

  window.speak = function(text) {
    msg.text = text;
    window.speechSynthesis.speak(msg);
  }
}

