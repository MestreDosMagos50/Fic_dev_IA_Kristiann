# 5. Git: Versionamento Profissional do Projeto

Abaixo estão os comandos exemplificados na aula para lidar com o versionamento usando Git.

## 5.1 Inicializando o Repositório
```bash
git init
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
git status
```

## 5.2 O Arquivo .gitignore
Criar o arquivo `.gitignore` com as pastas a ignorar (como `.venv/`, `__pycache__`, etc.).

## 5.3 Commits Semânticos
```bash
git add .gitignore .env.example
git commit -m "chore: configurar gitignore e env de exemplo"

git add backend/
git commit -m "feat: criar backend FastAPI com endpoint /ask"
```

## 5.4 Branches: Trabalhando em Paralelo
```bash
git switch -c feature/retriever-rag
git add chains/retriever_chain.py
git commit -m "feat: adicionar retriever RAG com FAISS"
git switch main
git merge feature/retriever-rag
git branch -d feature/retriever-rag
```

## 5.5 Tags de Versão
```bash
git tag -a v1.0.0 -m "MVP: assistente de Python com OpenAI + LangChain + FastAPI + Streamlit"
git push origin v1.0.0
```
