# VoiceBot

VoiceBot is an interactive conversational AI application designed to enhance user communication through both text and voice inputs. This project integrates advanced text and speech technologies to offer a seamless and engaging experience. Users can interact with the bot either by typing their messages or speaking directly into their devices.

## Key Features

- **Text Communication:** Users can type messages to the bot and receive immediate, contextually relevant responses.
- **Voice Interaction:** By utilizing Speech-to-Text (STT) technology, users can speak to the bot, which will transcribe their spoken words into text for processing.
- **Text-to-Speech (TTS):** The bot can convert its text responses into speech, allowing users to hear the bot’s replies, enhancing the interactivity of the conversation.
- **Dynamic Theme Toggle:** Users have the option to switch between light and dark themes for a personalized visual experience.

## Technologies

- **Backend:** Developed using Flask (Python), which manages API requests and interactions.
- **STT:** Employs the `speech_recognition` library to transcribe audio input into text.
- **TTS:** Utilizes `pyttsx3` for converting text responses into spoken audio.
- **Frontend:** Crafted with HTML, CSS, and JavaScript to deliver an intuitive user interface.

## How to Use

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/iamrishu11/VoiceBot.git

2. **Navigate to Repository:**
   ```bash
   cd VoiceBot

3. **Set up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

5. **Run the Application**
   ```bash
   python app.py

Access the app locally at http://127.0.0.1:5000 or from other devices on the same network using your local IP address.

## API Endpoints

- **POST /process_text:** Send text messages to the bot and receive text responses.
- **POST /process_audio:** Send audio files to the bot; the bot will transcribe the audio and respond with an audio reply

## Contributing

We welcome contributions to enhance VoiceBot! To contribute:

- **Open an Issue:** Report bugs or request features.
- **Submit a Pull Request:** Propose changes or improvements.

Please follow the contribution guidelines provided in the repository.

## LICENSE

This project is licensed under the MIT License.

## Contact

1. **Repository URL:** Ensure that the GitHub URL (`https://github.com/iamrishu11/VoiceBot.git`) is correct and points to your repository.
2. **Email Address:** Replace `[rishankj749@gmail.com](mailto:rishankj749@gmail.com)` with your actual contact email or preferred contact method.
3. **License:** Make sure you have a `LICENSE` file in your repository if you include a license section.

Feel free to adjust or expand the sections based on additional features or requirements specific to your project!
