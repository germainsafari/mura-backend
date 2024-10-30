# backend/openai_handler.py
import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY

def get_gpt_response(user_input, conversation_history):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation_history + [{"role": "user", "content": user_input}]
    )
    return response['choices'][0]['message']['content']
