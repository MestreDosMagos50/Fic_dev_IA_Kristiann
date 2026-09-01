import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

config = types.GenerateContentConfig(
    system_instruction="Voce e um assistente educacional especializado em Python. Responda em portugues, de forma clara e com exemplos de codigo.",
    temperature=0.7,
)

chat = client.chats.create(model="gemini-3.6-flash", config=config)
resp = chat.send_message("O que e uma list comprehension em Python?")
print("TEXT sem max_tokens:", repr(resp.text))
print("FINISH REASON:", resp.candidates[0].finish_reason if resp.candidates else None)
