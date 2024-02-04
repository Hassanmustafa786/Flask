document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chat-box');
    const userForm = document.getElementById('user-input-form');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const voiceButton = document.getElementById('voice-button');
    const voiceAudio = document.getElementById('voice-audio');

    let recognition;
    let isVoiceInputEnabled = true;

    // Check if SpeechRecognition is supported
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = false;
        recognition.interimResults = false;
    } else {
        voiceButton.disabled = true;
        console.error('SpeechRecognition not supported. Voice input is disabled.');
    }

    // Function to speak a message
    function speakMessage(message) {
        const synth = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance(message);
        synth.speak(utterance);
    }

    voiceButton.addEventListener('click', function () {
        if (recognition && isVoiceInputEnabled) {
            voiceButton.textContent = 'Listening...';
            recognition.start();
        }
    });

    recognition.onresult = function (event) {
        const userVoiceInput = event.results[0][0].transcript;
        userInput.value = userVoiceInput;
        voiceButton.textContent = 'Start Voice Input';
        // Simulate form submission
        userForm.dispatchEvent(new Event('submit'));
    };

    recognition.onend = function () {
        voiceButton.textContent = 'Start Voice Input';
    };

    userForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const userMessage = userInput.value.trim();
        if (userMessage !== '') {
            appendMessage('User', userMessage, 'user-message');
            userInput.value = '';

            // Send user input to server
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `user_input=${encodeURIComponent(userMessage)}`,
            })
            .then(response => response.json())
            .then(data => {
                const botMessage = data.response;
                appendMessage('Chatbot', botMessage, 'bot-message');
                speakMessage(botMessage);
                if (botMessage.toLowerCase().includes('what is your name')) {
                    isVoiceInputEnabled = false; // Disable voice input after asking about the name
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    function appendMessage(sender, message, messageClass) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', messageClass);
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
