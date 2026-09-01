import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

PROMPT_SISTEMA = """Voce e um assistente educacional especializado na trilha
Python para Iniciantes. Sua missao e responder duvidas de alunos de forma
clara, didatica e com exemplos de codigo quando pertinente.
Sempre responda em portugues. Se nao souber a resposta, diga honestamente.
Contexto adicional: {contexto}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", PROMPT_SISTEMA),
    ("human", "{pergunta}"),
])

modelo = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
    temperature=0.7,
)

chain = prompt | modelo | StrOutputParser()

def responder(pergunta: str, contexto: str = "") -> str:
    """Executa a chain com a pergunta e contexto fornecidos."""
    return chain.invoke({"pergunta": pergunta, "contexto": contexto})
