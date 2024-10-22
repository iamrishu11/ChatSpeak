from flask import Flask, request, jsonify, render_template, send_file
import io
import logging
import os
from datetime import datetime

# Import bot functions and database models
from burt import get_response, conversation_history
from models import ChatHistory, engine, Session, User
from auth_helpers import hash_password, verify_password

app = Flask(__name__, template_folder='templates', static_folder='static')

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

        return jsonify({'response_text': response_text})

    except Exception as e:
        logger.error(f"Error processing text: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/export_txt', methods=['POST'])
def export_txt():
    try:
        # Current time for the file name
        timestamp = datetime.now().strftime("%B_%d_%I-%M-%S_%p")
        file_name = f'chat_history_{timestamp}.txt'
        logger.info(f"File name: {file_name}")

        # Create the content of the text file from conversation history with timestamps
        file_content = ""
        for entry in conversation_history:
            timestamp_entry, content = entry.split(' - ', 1) if ' - ' in entry else ('', entry)
            if not timestamp_entry:
                timestamp_entry = datetime.now().strftime('%B %d %I:%M:%S %p')  # Add timestamp if none exists
            file_content += f"{timestamp_entry} - {content}\n"

        # Create a BytesIO object to serve as the file
        file_io = io.BytesIO(file_content.encode())
        
        # Send the file as an attachment with the correct filename
        return send_file(file_io, mimetype='text/plain', as_attachment=True, download_name=file_name)
    
    except Exception as e:
        logger.error(f"Error exporting text file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/export_db', methods=['POST'])
def export_db():
    session = Session()
    try:
        # Add conversation history to the database
        for entry in conversation_history:
            role, message = entry.split(":", 1)
            role = role.strip()
            message = message.strip()
            chat_entry = ChatHistory(role=role, message=message, user_id=1)  # Ensure user_id is set
            session.add(chat_entry)
        session.commit()

        # Ensure the database file exists
        db_file_path = 'chat_history.db'
        if not os.path.exists(db_file_path):
            raise FileNotFoundError(f"Database file '{db_file_path}' does not exist.")

        # Send the file as an attachment with the correct filename
        return send_file(db_file_path, mimetype='application/x-sqlite3', as_attachment=True, download_name=db_file_path)

    except Exception as e:
        logger.error(f"Error exporting to database: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    if not email or not password or not confirm_password:
        return jsonify({'error': 'All fields are required'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    hashed_password = hash_password(password)

    session = Session()
    try:
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400

        new_user = User(email=email, password=hashed_password)
        session.add(new_user)
        session.commit()
        return jsonify({'message': 'Signup successful'})
    except Exception as e:
        logger.error(f"Error during signup: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    session = Session()
    try:
        user = session.query(User).filter_by(email=email).first()
        if not user or not verify_password(user.password, password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Here, you might set a session or JWT token to keep the user logged in
        return jsonify({'message': 'Login successful'})
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
