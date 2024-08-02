# ChatSpeak 🤖

ChatSpeak is an interactive conversational AI application designed to enhance user communication through both text and voice inputs. This project integrates advanced text and speech technologies to offer a seamless and engaging experience. Users can interact with the bot either by typing their messages or speaking directly into their devices.

![Dark-Theme-Website-UI](static/images/dark-theme.png)
![light-Theme-Website-UI](static/images/light-theme.png)

![dark-theme](https://github.com/user-attachments/assets/8a535e6d-1b3d-413c-9cfc-25f8650099e3)

## Key Features 😎

- **Text Communication:** Users can type messages to the bot and receive immediate, contextually relevant responses.
- **Voice Interaction:** By utilizing Speech-to-Text (STT) technology, users can speak to the bot, which will transcribe their spoken words into text for processing.
- **Text-to-Speech (TTS):** The bot can convert its text responses into speech, allowing users to hear the bot’s replies, enhancing the interactivity of the conversation.
- **Dynamic Theme Toggle:** Users have the option to switch between light and dark themes for a personalized visual experience.

## Technologies 🖥️

- **Backend:** Developed using Flask (Python), which manages API requests and interactions.
- **STT:** Employs the `speech_recognition` library to transcribe audio input into text.
- **TTS:** Utilizes `pyttsx3` for converting text responses into spoken audio.
- **Frontend:** Crafted with HTML, CSS, and JavaScript to deliver an intuitive user interface.

## How to Use 🚀

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/iamrishu11/ChatSpeak.git

2. **Navigate to Repository:**
   ```bash
   cd ChatSpeak

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

## Project Structure 📂

This project is as structured as follows:
   ```bash
   ChatSpeak/
   │
   ├── app.py                # Main application file
   ├── bot.py                # loop bot logic
   ├── burt.py               # Bot file for app.py
   ├── config.json           # Configuration file for the bot
   ├── requirements.txt      # List of project dependencies
   │
   ├── templates/            # HTML templates for rendering views
   │   └── index.html        # Main HTML file
   │
   ├── static/               # Static files (CSS, JavaScript, images, etc.)
   │   ├── favicon.ico       # Favicon for the web app
   │   ├── styles.css        # CSS stylesheets
   │   └── script.js         # JavaScript files
   │
   ├── test/                 # Test-related files
   │   ├── test.html         # HTML files for testing
   │   ├── cURL-testing.txt  # Text file with cURL commands or test data
   │   └── test.py           # Python scripts for testing
   │
   ├── __pycache__/          # Compiled Python files
   │   ├── app.cpython-312.pyc
   │   ├── bot.cpython-312.pyc
   │   ├── burt.cpython-312.pyc
   │   └── test.cpython-312.pyc
   │
   ├── .gitignore            # Specifies files and directories to ignore in Git
   ├── README.md             # Project overview and documentation
   └── LICENSE               # License for the project
   ```

## API Endpoints 🔌

- **POST /process_text:** Send text messages to the bot and receive text responses.
- **POST /process_audio:** Send audio files to the bot; the bot will transcribe the audio and respond with an audio reply.

## Contributing 🤝

We welcome contributions to enhance ChatSpeak! To contribute:

- **Open an Issue:** Report bugs or request features.
- **Submit a Pull Request:** Propose changes or improvements.

Please follow the contribution guidelines provided in the repository.

## LICENSE 🧾

This project is licensed under the [MIT License](LICENSE).

## Contact 💬

For any inquiries, please contact [ME](mailto:rishankj749@gmail.com).

Feel free to adjust or expand the sections based on additional features or requirements specific to your project!
