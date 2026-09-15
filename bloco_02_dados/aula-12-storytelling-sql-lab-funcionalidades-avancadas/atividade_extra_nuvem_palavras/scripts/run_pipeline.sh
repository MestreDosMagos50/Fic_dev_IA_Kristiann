#!/usr/bin/env bash
# Script para inicialização e execução do pipeline periódico da Nuvem de Palavras

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=================================================================="
echo "🚀 Iniciando Pipeline da Nuvem de Palavras Tech (Aula 12)"
echo "=================================================================="

# 1. Ativar ambiente virtual caso exista
if [ -d "venv" ]; then
    echo "📦 Ativando ambiente virtual venv..."
    source venv/bin/activate
fi

# 2. Inicializar tabelas no banco de dados
echo "🗄️ Inicializando tabelas no PostgreSQL..."
python3 -c "import sys; sys.path.append('backend'); from database import init_tables; init_tables()"

# 3. Rodar worker periódico (a cada 5 minutos)
echo "⏱️ Iniciando worker em loop contínuo..."
python3 backend/worker.py
