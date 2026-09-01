# 2.3 Retriever: Respondendo com Base em Documentos
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# --- Criando a base de conhecimento a partir de textos locais ---
documentos_brutos = [
    "List comprehension e uma forma concisa de criar listas em Python. ",
    "Exemplo: quadrados = [x**2 for x in range(10)]",
    "Decoradores sao funcoes que modificam o comportamento de outras funcoes.",
    "O FastAPI e um framework moderno para criar APIs REST com Python.",
    "O Pandas e usado para manipulacao e analise de dados tabulares.",
]

# Dividir textos em chunks (fragmentos) menores para indexacao
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = splitter.create_documents(documentos_brutos)

# Criar embeddings (representacoes vetoriais) e indexar no FAISS
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# Retriever: busca os 3 chunks mais similares a pergunta
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --- Montando a chain RAG ---
prompt_rag = ChatPromptTemplate.from_messages([
    ("system",
     "Responda a pergunta usando APENAS o contexto abaixo.\n"
     "Se a resposta nao estiver no contexto, diga: 'Nao tenho informacao sobre isso.'\n"
     "Contexto:\n{contexto}"),
    ("human", "{pergunta}"),
])

modelo = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0.3)

def formatar_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Chain RAG completa
chain_rag = (
    {"contexto": retriever | formatar_docs, "pergunta": RunnablePassthrough()}
    | prompt_rag
    | modelo
    | StrOutputParser()
)

def responder_com_docs(pergunta: str) -> str:
    return chain_rag.invoke(pergunta)

if __name__ == "__main__":
    r = responder_com_docs("O que é FastAPI?")
    print(r)
