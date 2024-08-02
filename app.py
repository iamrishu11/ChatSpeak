from flask import Flask, request, jsonify, send_file, render_template, Response
import io
import pyttsx3
import speech_recognition as sr
import logging
import os
import time

# Import bot functions and database models
from burt import get_response, conversation_history
# from models import ChatHistory, engine, Session

app = Flask(__name__, template_folder='templates', static_folder='static')

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize STT (Speech-to-Text) and TTS (Text-to-Speech)
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Generate response text
        response_text = get_response(text)
        logger.info(f"Bot: {response_text}")

        # Convert response text to speech
        response_audio_path = 'static/response.mp3'
        tts_engine.save_to_file(response_text, response_audio_path)
        tts_engine.runAndWait()

        # Return both text and audio
        return jsonify({
            'response_text': response_text,
            'audio_url': '/static/response.mp3'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # Clean up the audio file
        if os.path.exists(response_audio_path):
            try:
                os.remove(response_audio_path)
            except Exception as e:
                logger.error(f"Error removing file: {e}")

@app.route('/process_audio', methods=['POST'])
def process_audio():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({'error': 'No audio file provided'}), 400

    try:
        audio = audio_file.read()
        with sr.AudioFile(io.BytesIO(audio)) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            logger.info(f"You: {text}")

        response_text = get_response(text)
        logger.info(f"Bot: {response_text}")

        # Convert response text to speech
        response_audio_path = 'static/response.mp3'
        tts_engine.save_to_file(response_text, response_audio_path)
        tts_engine.runAndWait()

        # Return both text and audio
        return jsonify({
            'response_text': response_text,
            'audio_url': 'static/response.mp3'
        })

    except sr.UnknownValueError:
        return jsonify({'error': 'Speech was unintelligible'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Speech recognition request error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_txt', methods=['POST'])
def export_txt():
    file_content = "\n".join(conversation_history)
    file_name = f'chat_history_{int(time.time())}.txt'
    return send_file(io.BytesIO(file_content.encode()), mimetype='text/plain', as_attachment=True, download_name=file_name)

"""
@app.route('/export_db', methods=['POST'])
def export_db():
    # Initialize a new database session
    session = Session()
    try:
        # Add conversation history to the database
        for entry in conversation_history:
            role, message = entry.split(":", 1)
            role = role.strip()
            message = message.strip()
            chat_entry = ChatHistory(role=role, message=message)
            session.add(chat_entry)
        session.commit()

        # Create a file to download
        db_file_path = 'chat_history.db'
        return send_file(db_file_path, mimetype='application/x-sqlite3', as_attachment=True, download_name=db_file_path)
    except Exception as e:
        logger.error(f"Error exporting to database: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
