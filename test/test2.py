import speech_recognition as sr
import time
import pyttsx3

def recognize_speech_from_microphone():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Listening...")
        
        start_time = time.time()
        
        try:
            audio_data = recognizer.listen(source)  # Capture audio from the microphone
            text = recognizer.recognize_google(audio_data)  # Recognize speech using Google API
            
        except sr.UnknownValueError:
            text = "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            text = f"Could not request results from Google Speech Recognition service; {e}"
        except Exception as e:
            text = f"An error occurred: {e}"
        
        end_time = time.time()
        print(f"Speech recognition took {end_time - start_time} seconds")
        
        return text

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
"""
# Example usage
result = recognize_speech_from_microphone()
print("You said:", result)
speak_text(result)
"""
speak_text("pyttsx3")