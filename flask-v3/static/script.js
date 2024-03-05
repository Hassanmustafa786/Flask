document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chat-box');
    const userForm = document.getElementById('user-input-form');
    const userInput = document.getElementById('user-input');
    const voiceButton = document.getElementById('voice-button');

    let recognition;
    let isVoiceInputEnabled = true;

    // Handle language selection change
    const languageSelect = document.getElementById('language-select');
    languageSelect.addEventListener("select-voice", function () {
        const selectedLanguage = languageSelect.value;
        console.log('Selected language:', selectedLanguage);
    });

    // Voice selection code
    let speech = new SpeechSynthesisUtterance();
    let voices = [];
    let voiceSelect = document.getElementById("select-voice");

    window.speechSynthesis.onvoiceschanged = () => {
        voices = window.speechSynthesis.getVoices();
        speech.voice = voices[0];

        voices.forEach((voice, i) => (voiceSelect.options[i] = new Option(voice.name, i)));
    };

    voiceSelect.addEventListener('change', () => {
        speech.voice = voices[voiceSelect.value];
    });

    document.getElementById("select-voice").addEventListener('change',()=>{
        speech.text=document.getElementById("initial-message").textContent;
        window.speechSynthesis.speak(speech);
    });

    // Check if SpeechRecognition is supported
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = false;
        recognition.interimResults = false;
    } else {
        voiceButton.disabled = true;
        console.error('SpeechRecognition not supported. Voice input is disabled.');
    };

    // Function to speak a message
    function speakMessage(message, voice) {
        const synth = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance(message);
        utterance.voice = voice; // Set the selected voice
        synth.speak(utterance);
    };

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
        voiceButton.textContent = '🎙️';
    };

    userForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const userMessage = userInput.value.trim();
        if (userMessage !== '') {
            appendMessage('You', userMessage, 'user-message');
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
                appendMessage('🤖', botMessage, 'bot-message');
                speakMessage(botMessage, voices[voiceSelect.value]); // Pass selected voice
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
    };
    
});

function submitForm() {
    document.getElementById("myForm").submit();
};

function submitVoice() {
    document.getElementById("select-voice").submit();
};