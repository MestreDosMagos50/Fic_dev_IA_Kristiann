# 3.1 Estrutura do Backend
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(
    title="Assistente Python API",
    description="Backend do assistente educacional de Python com LangChain",
    version="1.0.0",
)

# Permitir requisicoes do Streamlit (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"], # porta padrao do Streamlit
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# --- Modelos de dados (Pydantic) ---
class Pergunta(BaseModel):
    texto: str = Field(..., min_length=3, max_length=1000,
                       description="Pergunta do usuario")
    contexto: str = Field(default="", description="Contexto adicional opcional")

class Resposta(BaseModel):
    resposta: str
    modelo: str
    tokens_estimados: int

# --- Endpoints ---
@app.get("/")
def health_check():
    """Endpoint de verificacao de saude da API."""
    return {"status": "ok", "servico": "Assistente Python API"}

@app.post("/ask", response_model=Resposta)
def ask(pergunta: Pergunta):
    """
    Recebe uma pergunta e retorna a resposta gerada pelo LangChain.
    """
    try:
        # Aqui o backend do projeto final importaria a funcao do LangChain.
        # Por exemplo: from chains.qa_chain import responder
        # Aqui faremos uma simulacao para o script funcionar standalone:
        texto_resposta = f"Você perguntou: {pergunta.texto}" 
        
        return Resposta(
            resposta=texto_resposta,
            modelo="gpt-4o-mini",
            tokens_estimados=len(texto_resposta.split()) * 2,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("04_fastapi_backend:app", host="0.0.0.0", port=8000, reload=True)
