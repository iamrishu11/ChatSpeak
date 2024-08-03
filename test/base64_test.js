// Example Base64 audio data (replace with actual data)
const testAudioBase64 = 'aGVsbG8gdGhpcyBpcyB5b3VyIGJvaQ=='; // Replace with actual Base64 string

// Create the data URL for the audio
const testAudioUrl = `data:audio/wav;base64,${testAudioBase64}`;

// Create a new Audio object
const testAudio = new Audio(testAudioUrl);

// Add event listener to play the audio on button click
document.getElementById('playAudio').addEventListener('click', () => {
    testAudio.play().catch(error => {
        console.error('Test audio playback error:', error);
    });
});
