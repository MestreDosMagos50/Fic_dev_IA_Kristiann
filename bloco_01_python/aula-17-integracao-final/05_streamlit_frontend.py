# 4.1 Gerenciamento de Estado com session_state
import streamlit as st
import requests

# --- Configuração da página ---
st.set_page_config(
    page_title="Assistente Python",
    page_icon="🐍",
    layout="centered",
)

BACKEND_URL = "http://localhost:8000"

# --- Inicializar session_state ---
# Isso e executado apenas na primeira vez que o usuario abre a pagina
if "historico" not in st.session_state:
    st.session_state.historico = [] # lista de dicts: {role, content}

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
st.title("🐍 Assistente Python")
st.caption("Tire suas duvidas sobre Python com suporte de IA")
st.divider()

# Exibir historico de mensagens
for msg in st.session_state.historico:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Campo de entrada do usuario
if pergunta := st.chat_input("Digite sua duvida sobre Python..."):
    # Exibir mensagem do usuario
    with st.chat_message("user"):
        st.markdown(pergunta)
    
    # Salvar no historico
    st.session_state.historico.append({"role": "user", "content": pergunta})
    
    # Chamar backend e exibir resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            resposta = chamar_backend(pergunta)
            st.markdown(resposta)
            
    # Salvar resposta no historico
    st.session_state.historico.append({"role": "assistant", "content": resposta})

# Botao para limpar historico
if st.session_state.historico:
    if st.button("Limpar conversa", type="secondary"):
        st.session_state.historico = []
        st.rerun()
