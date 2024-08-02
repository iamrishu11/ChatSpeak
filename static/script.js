let mediaRecorder;
let audioChunks = [];

// Handle DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const textInput = document.getElementById('textInput');
    const sendTextButton = document.getElementById('sendText');
    const micIcon = document.getElementById('micIcon');
    const currentTheme = localStorage.getItem('theme') || 'light-theme';
    const menuIcon = document.getElementById('menuIcon');
    const menuContent = document.getElementById('menuContent');

    // Apply the current theme
    document.body.classList.add(currentTheme);

    // Function to update emoji colors and trigger animations
    function updateEmojiColors() {
        const sunEmoji = document.querySelector('.theme-toggle .sun');
        const moonEmoji = document.querySelector('.theme-toggle .moon');

        if (sunEmoji && moonEmoji) {
            if (document.body.classList.contains('dark-theme')) {
                sunEmoji.style.color = '#f0f0f0'; // Light color for sun in dark theme
                moonEmoji.style.color = '#fff'; // Dark color for moon in dark theme
                sunEmoji.style.transform = 'translateX(20px)'; // Slide sun emoji to the right
                moonEmoji.style.transform = 'translateX(-20px)'; // Slide moon emoji to the left
            } else {
                sunEmoji.style.color = '#333'; // Dark color for sun in light theme
                moonEmoji.style.color = '#333'; // Light color for moon in light theme
                sunEmoji.style.transform = 'translateX(-20px)'; // Slide sun emoji to the left
                moonEmoji.style.transform = 'translateX(20px)'; // Slide moon emoji to the right
            }
        }
    }

    // Initialize emoji colors and animations
    updateEmojiColors();

    // Toggle theme on button click
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            themeToggle.classList.add('cover-effect');
            setTimeout(() => {
                if (document.body.classList.contains('light-theme')) {
                    document.body.classList.remove('light-theme');
                    document.body.classList.add('dark-theme');
                    localStorage.setItem('theme', 'dark-theme');
                } else {
                    document.body.classList.remove('dark-theme');
                    document.body.classList.add('light-theme');
                    localStorage.setItem('theme', 'light-theme');
                }
                themeToggle.classList.remove('cover-effect');
                updateEmojiColors();
            }, 300); // Delay should match CSS transition duration
        });
    }

    // Handle text input submission
    if (sendTextButton) {
        sendTextButton.addEventListener('click', () => {
            const userInput = textInput.value.trim();
            if (userInput) {
                processUserInput(userInput); // Start processing the input
                textInput.value = ''; // Clear the input field after submission
            }
        });
    }

    // Handle Enter key for text input
    document.addEventListener('keydown', event => {
        if (event.key === 'Enter') {
            const input = textInput.value.trim();
            if (input) {
                processUserInput(input); // Start processing the input
                textInput.value = '';
            }
        }
    });

    // Handle microphone icon click for recording
    if (micIcon) {
        micIcon.addEventListener('click', async () => {
            if (mediaRecorder && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                micIcon.textContent = '🎙️'; // Change icon back to unrecording state
            } else {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);

                    mediaRecorder.ondataavailable = event => {
                        audioChunks.push(event.data);
                    };

                    mediaRecorder.onstop = async () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' }); // Ensure this MIME type matches server expectation
                        audioChunks = []; // Clear the chunks
                        micIcon.textContent = '🎙️'; // Change icon back to unrecording state

                        // Send audio to server for transcription
                        const formData = new FormData();
                        formData.append('audio', audioBlob, 'audio.wav');

                        try {
                            const response = await fetch('/process_audio', {
                                method: 'POST',
                                body: formData
                            });

                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }

                            const audioBlob = await response.blob(); // Get the audio response as a Blob
                            const audioUrl = URL.createObjectURL(audioBlob);
                            const audio = new Audio(audioUrl);
                            audio.play(); // Play the audio response

                        } catch (error) {
                            console.error('Error:', error);
                        }
                    };

                    mediaRecorder.start();
                    micIcon.textContent = '⏹️'; // Change icon to recording state
                } catch (error) {
                    console.error('Error accessing microphone:', error);
                }
            }
        });
    }
    
    // Handle menu visibility
    menuIcon.addEventListener('click', function() {
        // Toggle visibility of the menu
        if (menuContent.style.display === 'block') {
            menuContent.style.display = 'none';
        } else {
            menuContent.style.display = 'block';
        }
    });

    // Hide the menu if clicked outside of it
    document.addEventListener('click', function(event) {
        if (!menuIcon.contains(event.target) && !menuContent.contains(event.target)) {
            menuContent.style.display = 'none';
        }
    });

    // Add functionality for the export options
    document.getElementById('exportDatabase').addEventListener('click', function() {
        alert('Export as Database clicked');
        // Implement the export as database functionality
    });

    document.getElementById('exportTxt').addEventListener('click', function() {
        alert('Export as TXT clicked');
        // Implement the export as TXT functionality
    });
});

// Function to add a message to the chat
function addMessageToChat(message, isUser = false) {
    const chatContainer = document.getElementById('chatContainer');
    const welcomeMessage = document.getElementById('welcomeMessage');

    // Hide the welcome message when a new message is added
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }

    // Create the message element
    const messageElement = document.createElement('div');
    messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
    messageElement.textContent = message;

    // Add a gap after user messages
    if (isUser) {
        messageElement.classList.add('user-message-gap');
    }

    // Append the message to the chat container
    chatContainer.appendChild(messageElement);

    // Scroll to bottom of chat container
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Function to process user input
function processUserInput(input) {
    // Add the user's message to the chat
    addMessageToChat(`${input}`, true); // Sent by the user through text

    // Create a FormData object to send the input text to the server
    const formData = new FormData();
    formData.append('text', input);

    // Send a POST request to the server to process the text input
    fetch('/process_text', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.blob(); // Parse the response as a Blob
    })
    .then(blob => {
        // Create an object URL for the Blob and play the audio
        const audioUrl = URL.createObjectURL(blob);
        const audio = new Audio(audioUrl);
        audio.play();
    })
    .catch(error => {
        addMessageToChat('Sorry, something went wrong.');
        console.error('Error:', error);
    });
}
