# 1.2 Primeira Chamada à Gemini API (Atualizado para o novo SDK google-genai)
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# O cliente inicializa automaticamente usando a variável GEMINI_API_KEY do ambiente
client = genai.Client()

def perguntar(pergunta: str, historico: list = None) -> str:
    """Envia uma pergunta para a API do Gemini e retorna a resposta como string."""
    
    instrucao_sistema = (
        "Voce e um assistente educacional especializado em Python. "
        "Responda em portugues, de forma clara e com exemplos de codigo."
    )
    
    # Configuração de geração equivalente ao temperature e instrução
    config = types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        temperature=0.7,
    )

    modelo_gemini = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    
    # O SDK google-genai trabalha com sessões de chat.
    # Inicializamos o chat passando o modelo e as configurações.
    # (Para usar histórico preexistente, passaríamos history=... formatado como types.Content)
    chat = client.chats.create(model=modelo_gemini, config=config)
    
    # Envia a mensagem e recebe a resposta
    resposta = chat.send_message(pergunta)

    return resposta.text

# Teste rápido
if __name__ == "__main__":
    resposta = perguntar("O que e uma list comprehension em Python?")
    print(resposta)
