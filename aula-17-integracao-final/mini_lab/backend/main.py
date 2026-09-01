import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Adiciona o diretório raiz ao PYTHONPATH para permitir imports absolutos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chains.qa_chain import responder

app = FastAPI(
    title="Assistente Python API",
    description="Backend do assistente educacional de Python com LangChain",
    version="1.0.0"
)

# Permitir requisicoes do Streamlit (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pergunta(BaseModel):
    texto: str = Field(..., min_length=3, max_length=1000, description="Pergunta do usuario")
    contexto: str = Field(default="", description="Contexto adicional opcional")

class Resposta(BaseModel):
    resposta: str
    modelo: str
    tokens_estimados: int

@app.get("/")
def health_check():
    """Endpoint de verificacao de saude da API."""
    return {"status": "ok", "servico": "Assistente Python API", "versao": "1.0.0"}

@app.post("/ask", response_model=Resposta)
def ask(pergunta: Pergunta):
    """Recebe uma pergunta e retorna a resposta gerada pelo LangChain."""
    try:
        texto_resposta = responder(pergunta=pergunta.texto, contexto=pergunta.contexto)
        modelo_usado = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        return Resposta(
            resposta=texto_resposta, 
            modelo=modelo_usado,
            tokens_estimados=len(texto_resposta.split()) * 2
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
