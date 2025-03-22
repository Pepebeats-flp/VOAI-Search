import openai
import os

def setup_gpt():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("La variable OPENAI_API_KEY no está definida.")
    openai.api_key = key

def get_chat_completion(messages, model="gpt-4o"):
    setup_gpt()
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return response
    except Exception as e:
        print("Error al obtener la respuesta:", e)
        return None
