#!/usr/bin/env bash
# =============================================================================
# FIC Engenharia de Dados | Aula 04 (Módulo 2) / Aula 15
# Script: scripts/executar_workflow_hop.sh
# Objetivo: Executar o Workflow Mestre Big Data via Apache Hop Run (CLI)
# =============================================================================

set -e

DIR_ATUAL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOP_RUN_BIN="/home/ficdevia-16-tarde/Downloads/apache-hop-client-2.19.0/hop/hop-run.sh"

echo "======================================================================"
echo "🚀 EXECUTANDO WORKFLOW MESTRE BIG DATA VIA APACHE HOP RUN (CLI)"
echo "📄 Workflow: hop/workflows/workflow_bigdata_mestre.hwf"
echo "⚙️ Runtime: local"
echo "======================================================================"

PROJETO_NOME="${1:-1M de dados}"

if [ -f "${HOP_RUN_BIN}" ]; then
  "${HOP_RUN_BIN}" \
    -j "${PROJETO_NOME}" \
    -f "${DIR_ATUAL}/hop/workflows/workflow_bigdata_mestre.hwf" \
    -r local \
    -l BASIC
  echo "======================================================================"
  echo "✅ WORKFLOW MESTRE CONCLUÍDO COM SUCESSO PELO HOP-RUN!"
  echo "======================================================================"
else
  echo "ℹ️ Binário hop-run não encontrado no caminho padrão. Executando orquestrador Python equivalente..."
  python3 "${DIR_ATUAL}/scripts/executar_lab_completo.py"
fi
