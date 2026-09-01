import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# --- Configuração da página ---
st.set_page_config(
    page_title="Assistente Python",
    page_icon="🐍",
    layout="centered",
)

# --- Inicializar session_state ---
if "historico" not in st.session_state:
    st.session_state.historico = []

# --- Funcao de chamada ao backend ---
def chamar_backend(pergunta: str) -> str:
    try:
        response = requests.post(
            f"{BACKEND_URL}/ask",
            json={"texto": pergunta},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["resposta"]
    except requests.exceptions.ConnectionError:
        return "Erro: nao foi possivel conectar ao backend. Verifique se ele esta rodando."
    except requests.exceptions.Timeout:
        return "Erro: o backend demorou muito para responder. Tente novamente."
    except Exception as e:
        return f"Erro inesperado: {str(e)}"

# --- Interface ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🐍 Assistente Python")
    st.caption("MVP — Trilha Python para Iniciantes | Aula 17")
with col2:
    if st.button("Limpar", use_container_width=True):
        st.session_state.historico = []
        st.rerun()

st.divider()

# Exibir historico de mensagens
for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Campo de entrada do usuario
if pergunta := st.chat_input("Qual a sua duvida sobre Python?"):
    # Exibir mensagem do usuario
    with st.chat_message("user"):
        st.markdown(pergunta)
    
    # Salvar no historico
    st.session_state.historico.append({"role": "user", "content": pergunta})
    
    # Chamar backend e exibir resposta
    with st.chat_message("assistant"):
        with st.spinner("Consultando o assistente..."):
            resposta = chamar_backend(pergunta)
            st.markdown(resposta)
    
    # Salvar resposta no historico
    st.session_state.historico.append({"role": "assistant", "content": resposta})
