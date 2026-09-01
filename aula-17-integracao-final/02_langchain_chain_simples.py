# 2.2 Chain Simples de Pergunta e Resposta
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 1. Definir o prompt template
# {pergunta} e {contexto} serao substituidos dinamicamente
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Voce e um assistente especializado em Python para iniciantes. "
     "Use o contexto abaixo para responder. Se nao souber, diga que nao sabe.\n"
     "Contexto: {contexto}"),
    ("human", "{pergunta}"),
])

# 2. Instanciar o modelo
modelo = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"), temperature=0.7)

# 3. Parser de saída: converte o objeto AIMessage em string pura
parser = StrOutputParser()

# 4. Montar a chain com o operador pipe (|)
chain = prompt | modelo | parser

def responder(pergunta: str, contexto: str = "") -> str:
    """Executa a chain com a pergunta e contexto fornecidos."""
    return chain.invoke({
        "pergunta": pergunta,
        "contexto": contexto,
    })

if __name__ == "__main__":
    r = responder("O que e um decorador em Python?", contexto="")
    print(r)
