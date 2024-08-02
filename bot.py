""" 
   Main Bot Interactive Script with Speech Recognition and audio function

   File Name : 'bot.py'
   Author : 'Rishank Jain'

   Note : If your device does not have gpu but still want to run this bot comment the line '60'.

"""

import warnings
from concurrent.futures import ThreadPoolExecutor
import torch
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import speech_recognition as sr
import pyttsx3

# Suppress warnings from transformers
warnings.filterwarnings("ignore", message="1Torch was not compiled with flash attention", category=UserWarning)

# Load HF token from config.json
with open("config.json") as config_file:
    config_data = json.load(config_file)

HF_TOKEN = config_data["HF_TOKEN"]

# Model name
model_name = "Qwen/Qwen2-7B"

# Check for GPU availability and set device
if torch.cuda.is_available():
    print("GPU is available!")
    device = torch.device("cuda")
    print(torch.cuda.get_device_name(0))
else:
    print("GPU is not available. Please check your environment.")
    device = torch.device("cpu")

# Quantization configuration
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Loading tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name,
                                          token=HF_TOKEN,
                                          use_fast=True)

tokenizer.pad_token = tokenizer.eos_token  # Set pad token for end of sequence

print("Tokenizer is loaded.")

# Loading model with quantization configuration
try:
    model = AutoModelForCausalLM.from_pretrained(model_name,
                                                 quantization_config=bnb_config,
                                                 token=HF_TOKEN)
except ValueError as e:
    print(f"Error loading model: {e}")
    raise

print("Model is downloaded.")

# Initialize conversation history
conversation_history = []

# Setting up text generation pipeline
text_generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    do_sample=True,
    temperature=0.1,            # 'randomness' of outputs
    top_p=0.15,                 # select from top tokens whose probability add up to 15%
    top_k=25,                   # select from top 25 tokens
    max_new_tokens=256,         # max number of tokens to generate in the output
    repetition_penalty=1.1,      # penalty for repeated tokens
    truncation=True
)

print("Text generator is ready.")

# Initialize speech recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Initialize pyttsx3 TTS function
engine = pyttsx3.init()

# Function to generate response based on input prompt
def get_response(prompt):
    try:
        # Build the full prompt with conversation history
        context = "\n".join(conversation_history)
        full_prompt = f"{context}\nUser: {prompt}\nBot:"

        # Add prompt to conversation history
        conversation_history.append(f"User: {prompt}")
        
        # Generate response based on the full prompt
        sequences = text_generator(full_prompt)

        # Extract the generated response
        gen_text = sequences[0]['generated_text'].split("Bot:")[-1].strip()

        # Add generated response to conversation history
        conversation_history.append(f"Bot: {gen_text}")

        return gen_text

    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I couldn't understand that."

# Function to recognize speech and convert to text
def recognize_speech():
    with mic as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            return None

# Main loop for conversation
print("Bot is starting.\n")
print("You can say 'exit' to end the conversation.\n")

with ThreadPoolExecutor() as executor:
    while True:
        # Recognize speech input
        prompt = recognize_speech()

        if prompt is None:
            # If speech recognition fails, ask the user to try again
            print("Bot: Please speak again.")
            continue
        
        if prompt.lower() == "exit":
            print("Exiting the chatbot. Goodbye!")
            break

        if prompt.strip():  # Only process non-empty input
            # Generate response for the current prompt asynchronously
            future = executor.submit(get_response, prompt)
            output = future.result()

            # Print bot's response
            print("Bot:", output)

            engine.say(output)
            engine.runAndWait()
        else:
            print("Bot: Please say something.")

print("End of conversation.")
