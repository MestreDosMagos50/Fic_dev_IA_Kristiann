#!/usr/bin/env bash
# =============================================================================
# FIC Engenharia de Dados | Aula 03 (Módulo 2): Apache Hop & Orquestração
# Passo 4 — Desafio: Execução por Linha de Comando em Produção Simulada
# =============================================================================

set -e

DIR_ATUAL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOP_RUN_BIN="/home/ficdevia-16-tarde/Downloads/apache-hop-client-2.19.0/hop/hop-run.sh"

# Parâmetro default se não for passado: ano-mês atual ou 2026-08
MES_REF="${1:-2026-08}"

echo "======================================================================"
echo "🚀 EXECUTANDO WORKFLOW MESTRE VIA APACHE HOP RUN (CLI)"
echo "📁 Projeto: ecommerce"
echo "📄 Workflow: hop/workflows/carga_diaria.hwf"
echo "⚙️ Parâmetro MES_REF: ${MES_REF}"
echo "======================================================================"

"${HOP_RUN_BIN}" \
  -j ecommerce \
  -f "${DIR_ATUAL}/hop/workflows/carga_diaria.hwf" \
  -r local \
  -p "MES_REF=${MES_REF}" \
  -l BASIC

echo "======================================================================"
echo "✅ EXECUÇÃO CONCLUÍDA COM SUCESSO PELO HOP-RUN!"
echo "======================================================================"
