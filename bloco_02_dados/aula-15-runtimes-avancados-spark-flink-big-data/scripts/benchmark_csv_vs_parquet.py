#!/usr/bin/env python3
# =============================================================================
# FIC Engenharia de Dados | Aula 04 (Módulo 2) / Aula 15
# Script: scripts/benchmark_csv_vs_parquet.py
# Objetivo: Executar benchmark empírico CSV vs Parquet (Passo 2 do Mini-lab)
# =============================================================================

import os
import sys
import time
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.csv as pcsv

def run_benchmark():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file = os.path.join(base_dir, "dados", "entrada", "vendas_grandes.csv")
    parquet_file = os.path.join(base_dir, "dados", "saida", "vendas_grandes.parquet")
    metrics_json = os.path.join(base_dir, "dados", "saida", "metricas_benchmark.json")

    os.makedirs(os.path.dirname(parquet_file), exist_ok=True)

    if not os.path.exists(csv_file):
        print(f"❌ Arquivo CSV não encontrado: {csv_file}")
        print("Execute primeiro: python3 scripts/gera_vendas_grandes.py")
        sys.exit(1)

    print("=" * 75)
    print("⚡ PASSO 2 — BENCHMARK DE ALTA PERFORMANCE: CSV VS. PARQUET")
    print("=" * 75)

    # 1. Medir tamanho do CSV
    tamanho_csv_bytes = os.path.getsize(csv_file)
    tamanho_csv_mb = tamanho_csv_bytes / (1024 * 1024)
    print(f"📄 Arquivo CSV de Entrada: {tamanho_csv_mb:.2f} MB")

    # 2. Conversão CSV -> Parquet (Equivalente ao converte_parquet.hpl)
    print("\n🔄 1. Convertendo CSV -> Parquet (Compressão Snappy, Tipagem Forte)...")
    t0_conv = time.time()
    
    # Leitura com PyArrow otimizada em streaming
    table = pcsv.read_csv(csv_file)
    pq.write_table(table, parquet_file, compression='snappy')
    t_conversao = time.time() - t0_conv
    
    total_linhas = table.num_rows
    tamanho_parquet_bytes = os.path.getsize(parquet_file)
    tamanho_parquet_mb = tamanho_parquet_bytes / (1024 * 1024)
    taxa_compressao = (1 - (tamanho_parquet_bytes / tamanho_csv_bytes)) * 100

    print(f"✅ Conversão concluída em {t_conversao:.2f} s ({total_linhas:,} linhas)")
    print(f"📦 Tamanho Parquet: {tamanho_parquet_mb:.2f} MB (Redução de {taxa_compressao:.1f}%)")

    # 3. Teste A: Agregação lendo CSV (agrega_vendas_csv.hpl)
    # Agregação: Receita total por Categoria com Group By
    print("\n🧪 2. Testando Agregação lendo CSV (Receita por Categoria)...")
    t0_csv = time.time()
    df_csv = pd.read_csv(csv_file, usecols=["categoria", "receita"])
    agg_csv = df_csv.groupby("categoria")["receita"].sum().reset_index()
    t_csv_exec = time.time() - t0_csv
    vel_csv = total_linhas / t_csv_exec

    print(f"⏱️ Tempo Leitura + Agregação (CSV): {t_csv_exec:.3f} s")
    print(f"⚡ Throughput (CSV): {vel_csv:,.0f} linhas/s")

    # 4. Teste B: Agregação lendo Parquet (agrega_vendas_parquet.hpl)
    # Mesma agregação usando Projeção Colunar nativa do Parquet
    print("\n🧪 3. Testando Agregação lendo Parquet (Receita por Categoria)...")
    t0_parq = time.time()
    # Lê APENAS as duas colunas diretamente do disco
    table_parq = pq.read_table(parquet_file, columns=["categoria", "receita"])
    df_parq = table_parq.to_pandas()
    agg_parq = df_parq.groupby("categoria")["receita"].sum().reset_index()
    t_parq_exec = time.time() - t0_parq
    vel_parq = total_linhas / t_parq_exec

    print(f"⏱️ Tempo Leitura + Agregação (Parquet): {t_parq_exec:.3f} s")
    print(f"⚡ Throughput (Parquet): {vel_parq:,.0f} linhas/s")

    # Razão de ganho
    speedup = t_csv_exec / t_parq_exec if t_parq_exec > 0 else 0

    # 5. Tabela Comparativa (Exigida pelo PDF)
    print("\n" + "=" * 75)
    print("📊 TABELA COMPARATIVA OFICIAL DO PASSO 2:")
    print("=" * 75)
    print(f"{'Métrica':<30} | {'CSV':<18} | {'Parquet':<18} | {'Vantagem'}")
    print("-" * 75)
    print(f"{'Tamanho em disco':<30} | {tamanho_csv_mb:10.2f} MB      | {tamanho_parquet_mb:10.2f} MB      | {taxa_compressao:.1f}% menor")
    print(f"{'Tempo leitura + agregação':<30} | {t_csv_exec:10.3f} s       | {t_parq_exec:10.3f} s       | {speedup:.1f}x mais rápido")
    print(f"{'Linhas / segundo':<30} | {vel_csv:10,.0f} lin/s   | {vel_parq:10,.0f} lin/s   | +{vel_parq - vel_csv:,.0f} lin/s")
    print("=" * 75)

    # 6. Salvar Métricas Consolidadas para o Dashboard
    resultados = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_linhas": total_linhas,
        "csv": {
            "tamanho_mb": round(tamanho_csv_mb, 2),
            "tempo_segundos": round(t_csv_exec, 3),
            "linhas_por_segundo": int(vel_csv)
        },
        "parquet": {
            "tamanho_mb": round(tamanho_parquet_mb, 2),
            "tempo_segundos": round(t_parq_exec, 3),
            "linhas_por_segundo": int(vel_parq),
            "taxa_compressao_pct": round(taxa_compressao, 1),
            "speedup_fator": round(speedup, 2)
        },
        "categorias": agg_parq.to_dict(orient="records")
    }

    with open(metrics_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Métricas salvas em: {metrics_json}")
    return resultados

if __name__ == "__main__":
    run_benchmark()
