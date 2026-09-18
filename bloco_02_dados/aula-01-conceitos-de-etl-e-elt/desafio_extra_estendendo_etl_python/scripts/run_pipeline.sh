#!/usr/bin/env bash
# run_pipeline.sh — Execução Completa e Automatizada do Mini-lab
# Módulo 2 / Aula 01 — FIC Engenharia de Dados

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"
cd "$DIR"

echo "=================================================================="
echo "  DESAFIO EXTRA: ESTENDENDO O ETL EM PYTHON (MÓDULO 2 / AULA 01)"
echo "=================================================================="

# 1. Configuração do Ambiente Virtual
if [ ! -d ".venv" ]; then
    echo "[1/5] Criando ambiente virtual Python (.venv)..."
    python3 -m venv .venv
else
    echo "[1/5] Ambiente virtual (.venv) já existente."
fi

# Ativação do ambiente
source .venv/bin/activate

# 2. Instalação de Dependências
echo "[2/5] Instalando dependências..."
pip install --quiet -r requirements.txt

# 3. Inicialização de Tabelas no Banco
echo "[3/5] Verificando conexão e aplicando DDL no PostgreSQL..."
export PGPASSWORD=${PG_PASSWORD:-postgres}
psql -h ${PG_HOST:-localhost} -p ${PG_PORT:-5432} -U ${PG_USER:-postgres} -d ${PG_DB:-meu_banco_de_dados} -f scripts/init_db.sql > /dev/null 2>&1 || true

# 4. Execução do ETL com Desafios Implementados (Passos 3 e 4)
echo "[4/5] Executando pipeline ETL com os desafios (Passos 3 e 4)..."
python python/etl_produtos_desafio.py

# 5. Auditoria e Prova de Idempotência
echo "[5/5] Executando auditoria automatizada e prova de idempotência..."
python scripts/auditoria_etl.py

echo ""
echo "=================================================================="
echo "   PIPELINE E AUDITORIA CONCLUÍDOS COM SUCESSO!"
echo "=================================================================="
