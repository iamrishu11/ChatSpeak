"""import torch
import transformers


print(" Torch: ",torch.__version__)
print(torch.cuda.is_available())
print("Transformers: ",transformers.__version__)


# i think its downloaded

#yes let this program run plz this will ensure cuda working fine let it complete 
# it will take lot of time as it is first shard only 
# we can run my application ok sure


# bro now i caan remove myenv and what else?
#wait I after this shards download will complete then will come to know 
# after this try my program also 

#if you want can discunnect we can connect again if needed I think this should work 
# okay bro thank u so muchhhhh

# conda remove pytorch torchvision torchaudio pytorch-cuda

# conda clean --all

# pip uninstall accelerate gTTS transformers bitsandbytes SpeechRecognition pyaudio pydub

"""
"""
import speech_recognition as sr

def recognize_speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    print("Say 'exit' to stop the program.")

    while True:
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            
            # Capture the audio from the microphone
            audio = recognizer.listen(source)

            try:
                # Recognize speech using Google Web Speech API
                print("Recognizing...")
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")

                # Exit condition
                if "exit" in text.lower():
                    print("Exiting...")
                    break

            except sr.UnknownValueError:
                print("Google Web Speech API could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech API; {e}")

if __name__ == "__main__":
    recognize_speech()
"""

"""
import pyttsx3
engine = pyttsx3.init()

# Set the speaking rate
rate = engine.getProperty('rate')  # Get current speaking rate
print(f"Current rate: {rate}")     # Print the current voice rate

# Set a new speaking rate
engine.setProperty('rate', 175)    # Set new voice rate
rate = engine.getProperty('rate')  # Get updated speaking rate
print(f"Updated rate: {rate}")     # Print the updated voice rate

# Text to be spoken
text = ("When an advertiser places a bid on a keyword, they are essentially saying "
        "I'm willing to pay this much per click if someone clicks on my ad. The higher "
        "the bid, the more likely the ad will be displayed at the top of the SERP.")

# Start speaking the text
engine.say(text)
engine.runAndWait()

"""

import sounddevice as sd
import numpy as np
import io
import wave
import speech_recognition as sr

def recognize_speech():
    # Parameters
    samplerate = 16000
    chunk_size = samplerate  # Size of one second of audio

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Continuous recording loop
    print("Listening... Say 'exit' to stop.")

    with sd.InputStream(samplerate=samplerate, channels=1, dtype='int16') as stream:
        audio_buffer = io.BytesIO()

        while True:
            # Read audio data in chunks
            audio_chunk, _ = stream.read(chunk_size)  # Read one second of audio
            
            # Write the audio data to the buffer
            audio_buffer.write(audio_chunk)

            # Rewind buffer to start
            audio_buffer.seek(0)

            # Create in-memory WAV file and process it
            try:
                # Create a WAV file in memory
                with io.BytesIO() as wav_buffer:
                    with wave.open(wav_buffer, 'wb') as wav_file:
                        wav_file.setnchannels(1)
                        wav_file.setsampwidth(2)  # 16-bit audio
                        wav_file.setframerate(samplerate)
                        wav_file.writeframes(audio_chunk)

                    # Rewind the WAV buffer to the start
                    wav_buffer.seek(0)

                    # Process the WAV file
                    with sr.AudioFile(wav_buffer) as source:
                        audio = recognizer.record(source)
                        text = recognizer.recognize_google(audio)
                        print(f"You: {text}")

                        # Check for 'exit' command
                        if text.lower() == "exit":
                            print("Exiting...")
                            break
            except sr.UnknownValueError:
                # Ignore unrecognized speech
                pass
            except sr.RequestError as e:
                print(f"Sorry, there was an error with the speech recognition service: {e}")

            # Reset buffer for next chunk
            audio_buffer.seek(0)
            audio_buffer.truncate()

if __name__ == "__main__":
    recognize_speech()

"""
import pyaudio

def test_microphone():
    p = pyaudio.PyAudio()

    try:
        # Open a stream with the default microphone
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        print("Microphone is working.")

        # Read a small chunk of audio data
        data = stream.read(1024)
        print("Received audio data.")

        # Close the stream
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Error with microphone: {e}")
    finally:
        p.terminate()

# Run the test
if __name__ == "__main__":
    test_microphone()
"""