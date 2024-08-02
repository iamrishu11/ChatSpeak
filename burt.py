import warnings
from concurrent.futures import ThreadPoolExecutor
import torch
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import speech_recognition as sr
import pyttsx3
import logging

# Suppress warnings from transformers
warnings.filterwarnings("ignore", message=".*Torch was not compiled with flash attention.*", category=UserWarning)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load HF token from config.json
try:
    with open("config.json") as config_file:
        config_data = json.load(config_file)
    HF_TOKEN = config_data["HF_TOKEN"]
except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    logger.error(f"Error loading config: {e}")
    raise

# Model name
model_name = "Qwen/Qwen2-7B"

# Check for GPU availability and set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Device set to: {device}")

# Quantization configuration
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Loading tokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN, use_fast=True)
    tokenizer.pad_token = tokenizer.eos_token  # Set pad token for end of sequence
    logger.info("Tokenizer loaded successfully.")
except Exception as e:
    logger.error(f"Error loading tokenizer: {e}")
    raise

# Loading model with quantization configuration
try:
    model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config, token=HF_TOKEN)
    logger.info("Model loaded successfully.")
except ValueError as e:
    logger.error(f"Error loading model: {e}")
    raise

# Initialize conversation history
conversation_history = []

# Setting up text generation pipeline
text_generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    do_sample=True,
    temperature=0.1,
    top_p=0.15,
    top_k=25,
    max_new_tokens=256,
    repetition_penalty=1.1,
    truncation=True
)

logger.info("Text generator is ready.")

# Initialize speech recognizer
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Initialize pyttsx3 TTS function
engine = pyttsx3.init()

# Function to generate response based on input prompt
def get_response(prompt):
    try:
        context = "\n".join(conversation_history)
        full_prompt = f"{context}\nUser: {prompt}\nBot:"

        conversation_history.append(f"User: {prompt}")
        sequences = text_generator(full_prompt)
        gen_text = sequences[0]['generated_text'].split("Bot:")[-1].strip()
        conversation_history.append(f"Bot: {gen_text}")

        return gen_text

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "I'm sorry, I couldn't understand that."

# Function to recognize speech and convert to text
def recognize_speech():
    with mic as source:
        logger.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio)
            logger.info(f"You: {text}")
            return text
        except sr.UnknownValueError:
            logger.warning("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Web Speech API; {e}")
            return None
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out. No speech detected.")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in speech recognition: {e}")
            return None

# Optionally, you can add a main loop for interactive use, but for Flask, it’s not needed here.
# This part can be used in a script if you want an interactive bot.
