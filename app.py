from flask import Flask, request, jsonify, send_file, render_template
import io
import pyttsx3
import speech_recognition as sr
import logging
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize STT (Speech-to-Text) and TTS (Text-to-Speech)
recognizer = sr.Recognizer()
mic = sr.Microphone()
engine = pyttsx3.init()

# Import the bot logic
from burt import get_response

@app.route('/')
def index():
    return render_template('index.html')

def process_text_and_send_response(text):
    return get_response(text)

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        response_text = process_text_and_send_response(text)
        logger.info(f"Bot: {response_text}")
        return jsonify({'response': response_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/process_audio', methods=['POST'])
def process_audio():
    """
    Receives an audio file, processes it to convert to text, generates a response,
    converts the response text to audio, and returns the audio file.
    """
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({'error': 'No audio file provided'}), 400

    # Convert audio file to text using STT
    try:
        audio = audio_file.read()
        with sr.AudioFile(io.BytesIO(audio)) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            logger.info(f"You: {text}")
    except sr.UnknownValueError:
        return jsonify({'error': 'Speech was unintelligible'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Speech recognition request error: {e}'}), 500

    # Generate response using model
    try:
        response_text = process_text_and_send_response(text)
        logger.info(f"Bot: {response_text}")
    except Exception as e:
        logger.error(f"Error in processing text: {e}")
        return jsonify({'error': str(e)}), 500

    # Convert response text to speech using TTS
    response_audio_path = 'response.mp3'
    try:
        engine.save_to_file(response_text, response_audio_path)
        engine.runAndWait()
        return send_file(response_audio_path, mimetype='audio/mpeg', as_attachment=True)
    except Exception as e:
        logger.error(f"Error in generating speech: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the file after sending
        if os.path.exists(response_audio_path):
            try:
                os.remove(response_audio_path)
            except Exception as e:
                logger.error(f"Error removing file: {e}")

if __name__ == '__main__':
    # Initialize the bot
    try:
        get_response("initializing")  # Initialize or preload if needed
    except Exception as e:
        logger.error(f"Error initializing the bot: {e}")
    app.run(host='0.0.0.0', port=5000, debug=True)

