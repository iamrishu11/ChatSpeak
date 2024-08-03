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
    const exportTxtButton = document.getElementById('exportTxt');
    const exportDbButton = document.getElementById('exportDatabase');

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
    
                        // Add a placeholder message to the chat container
                        addMessageToChat('Processing your audio message...', true);
    
                        const formData = new FormData();
                        formData.append('audio', audioBlob, 'audio.wav');
    
                        try {
                            const response = await fetch('/process_audio_file', {
                                method: 'POST',
                                body: formData
                            });
    
                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }
    
                            const { response_text, audio_base64 } = await response.json(); // Expect JSON response from server
    
                            // Update the placeholder message to display the recognized text
                            addMessageToChat(`Recognized text: ${response_text}`, false);
    
                            // Play the audio
                            const audio = new Audio(`data:audio/wav;base64,${audio_base64}`);
                            audio.play();
    
                        } catch (error) {
                            console.error('Error:', error);
                            addMessageToChat('Sorry, something went wrong with processing your audio.', true);
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

    // Handle export as TXT button click
    if (exportTxtButton) {
        exportTxtButton.addEventListener('click', async () => {
            if (isChatContainerEmpty()) {
                alert('No chat content available to export.');
                return;
            }
            
            try {
                const response = await fetch('/export_txt', {
                    method: 'POST'
                });
    
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
    
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);

                // Extract the filename from the response headers or use a predefined format
                const disposition = response.headers.get('Content-Disposition');
                let filename = 'chat_history.txt'; // Default filename if not found in headers
                if (disposition && disposition.indexOf('attachment') !== -1) {
                    const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    const matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) {
                        filename = matches[1].replace(/['"]/g, '');
                    }
                }

                const link = document.createElement('a');
                link.href = url;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
    
            } catch (error) {
                console.error('Error:', error);
                alert('Sorry, something went wrong with exporting the chat history.');
            }
        });
    }

    // Handle export as Database button click
    if (exportDbButton) {
        exportDbButton.addEventListener('click', async () => {
            if (isChatContainerEmpty()) {
                alert('No chat content available to export.');
                return;
            }

            try {
                const response = await fetch('/export_db', {
                    method: 'POST'
                });
    
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
    
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = 'chat_history.db';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                URL.revokeObjectURL(url);
    
            } catch (error) {
                console.error('Error:', error);
                alert('Sorry, something went wrong with exporting the chat history.');
            }
        });
    }
});

// Function to check if chat container is empty, excluding the welcomeMessage div
function isChatContainerEmpty() {
    const chatContainer = document.getElementById('chatContainer');
    const welcomeMessage = document.getElementById('welcomeMessage');
    
    // Check if there are any children elements other than welcomeMessage
    return Array.from(chatContainer.children).every(child => child === welcomeMessage);
}

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

// Function to process user input and display response
async function processUserInput(input) {
    addMessageToChat(`${input}`, true);

    try {
        const response = await fetch('/process_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ text: input })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const { response_text } = await response.json();

        // Display bot response
        addMessageToChat(`${response_text}`, false);

        // Generate and play audio response
        const audioResponse = await fetch('/process_audio', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ text: response_text })
        });

        if (!audioResponse.ok) {
            throw new Error('Network response was not ok');
        }

        const { audio_base64 } = await audioResponse.json();
        const audio = new Audio(`data:audio/wav;base64,${audio_base64}`);
        audio.play();

    } catch (error) {
        console.error('Error:', error);
        addMessageToChat('Sorry, something went wrong with processing your text.', false);
    }
}
