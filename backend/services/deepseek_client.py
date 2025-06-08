import openai
from dotenv import load_dotenv
load_dotenv()  # Esto carga el archivo .env
import os


def setup_deepseek():
    # Configura la API key y la URL base para DeepSeek
    openai.api_key = os.getenv("DEEPSEEK_API_KEY")
    openai.api_base = "https://api.deepseek.com"

def get_chat_completion(messages, model="deepseek-reasoner"):
    setup_deepseek()
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response
