#!/usr/bin/env python3
# =============================================================================
# FIC Engenharia de Dados | Aula 04 (Módulo 2) / Aula 15
# Script: scripts/responder_desafios_negocio.py
# Objetivo: Resolver as 3 perguntas de negócio e salvar Parquet particionado por mês
# =============================================================================

import os
import sys
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def resolver_desafios():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parquet_in = os.path.join(base_dir, "dados", "saida", "vendas_grandes.parquet")
    output_particionado = os.path.join(base_dir, "dados", "saida", "particionado_ano_mes")
    output_json = os.path.join(base_dir, "dados", "saida", "respostas_desafios.json")

    print("=" * 75)
    print("💼 PASSO 4 — DESAFIO DE ENGENHARIA: PERGUNTAS DE NEGÓCIO EM PARQUET")
    print("=" * 75)

    if not os.path.exists(parquet_in):
        print(f"❌ Arquivo não encontrado: {parquet_in}")
        print("Execute os scripts anteriores primeiro.")
        sys.exit(1)

    # 1. Carregar dataset do Parquet via PyArrow (Projeção otimizada)
    print("📖 Carregando dataset analítico do Parquet...")
    cols = ["id_venda", "data_venda", "ano_mes", "produto", "categoria", "receita", "regiao"]
    df = pd.read_parquet(parquet_in, columns=cols)
    total_linhas = len(df)
    receita_total = df["receita"].sum()
    print(f"📊 Dataset carregado: {total_linhas:,} transações | Faturamento Total: R$ {receita_total:,.2f}")

    # -------------------------------------------------------------
    # PERGUNTA 1: TOP 10 PRODUTOS POR RECEITA
    # -------------------------------------------------------------
    print("\n🏆 [Pergunta 1] Calculando Top 10 Produtos por Receita...")
    top10_produtos = (
        df.groupby(["produto", "categoria"])["receita"]
        .agg(["sum", "count"])
        .reset_index()
        .rename(columns={"sum": "receita_total", "count": "total_pedidos"})
        .sort_values(by="receita_total", ascending=False)
        .head(10)
    )
    top10_produtos["share_receita_pct"] = (top10_produtos["receita_total"] / receita_total) * 100

    print("\n--- TOP 10 PRODUTOS ---")
    for idx, row in top10_produtos.reset_index(drop=True).iterrows():
        print(f"#{idx+1:02d} | {row['produto']:<35} | R$ {row['receita_total']:12,.2f} ({row['share_receita_pct']:.1f}%)")

    # -------------------------------------------------------------
    # PERGUNTA 2: TICKET MÉDIO POR REGIÃO E MÊS
    # -------------------------------------------------------------
    print("\n🗺️ [Pergunta 2] Calculando Ticket Médio por Região e Mês...")
    ticket_regional = (
        df.groupby(["ano_mes", "regiao"])
        .agg(receita_total=("receita", "sum"), total_pedidos=("id_venda", "count"))
        .reset_index()
    )
    ticket_regional["ticket_medio"] = ticket_regional["receita_total"] / ticket_regional["total_pedidos"]
    ticket_regional = ticket_regional.sort_values(by=["ano_mes", "ticket_medio"], ascending=[True, False])

    # Amostra dos últimos meses
    print("\n--- AMOSTRA TICKET MÉDIO (Último Mês Disponível) ---")
    ultimo_mes = ticket_regional["ano_mes"].max()
    amostra_ticket = ticket_regional[ticket_regional["ano_mes"] == ultimo_mes]
    for _, row in amostra_ticket.iterrows():
        print(f"Mês: {row['ano_mes']} | Região: {row['regiao']:<14} | Ticket Médio: R$ {row['ticket_medio']:8.2f} | Pedidos: {row['total_pedidos']:,}")

    # -------------------------------------------------------------
    # PERGUNTA 3: CRESCIMENTO MENSAL (Month-over-Month - MoM)
    # -------------------------------------------------------------
    print("\n📈 [Pergunta 3] Calculando Crescimento Mensal de Faturamento (MoM)...")
    crescimento_mensal = (
        df.groupby("ano_mes")["receita"]
        .agg(["sum", "count"])
        .reset_index()
        .rename(columns={"sum": "receita_mensal", "count": "total_transacoes"})
        .sort_values(by="ano_mes")
    )
    crescimento_mensal["receita_mes_anterior"] = crescimento_mensal["receita_mensal"].shift(1)
    crescimento_mensal["crescimento_mom_pct"] = (
        (crescimento_mensal["receita_mensal"] - crescimento_mensal["receita_mes_anterior"])
        / crescimento_mensal["receita_mes_anterior"]
    ) * 100
    crescimento_mensal["crescimento_mom_pct"] = crescimento_mensal["crescimento_mom_pct"].fillna(0.0)

    print("\n--- CRESCIMENTO MÊS A MÊS ---")
    for _, row in crescimento_mensal.iterrows():
        sinal = "+" if row["crescimento_mom_pct"] >= 0 else ""
        print(f"Mês: {row['ano_mes']} | Receita: R$ {row['receita_mensal']:12,.2f} | MoM: {sinal}{row['crescimento_mom_pct']:6.2f}%")

    # -------------------------------------------------------------
    # EXPORTAÇÃO PARQUET PARTICIONADO POR MÊS (Hive Partitioning)
    # -------------------------------------------------------------
    print("\n💾 Exportando dataset completo em Parquet Particionado por Mês...")
    os.makedirs(output_particionado, exist_ok=True)
    
    # Criação da tabela PyArrow para particionamento nativo em alta velocidade
    table_full = pa.Table.from_pandas(df)
    pq.write_to_dataset(
        table_full,
        root_path=output_particionado,
        partition_cols=["ano_mes"],
        compression="snappy"
    )

    particoes_criadas = [p for p in os.listdir(output_particionado) if p.startswith("ano_mes=")]
    particoes_criadas.sort()
    print(f"✅ Sucesso! {len(particoes_criadas)} partições criadas em {output_particionado}:")
    for p in particoes_criadas[:4]:
        tam_kb = sum(os.path.getsize(os.path.join(output_particionado, p, f)) for f in os.listdir(os.path.join(output_particionado, p))) / 1024
        print(f"   📁 {p}/ ({tam_kb:.1f} KB)")
    if len(particoes_criadas) > 4:
        print(f"   ... e mais {len(particoes_criadas) - 4} partições mensais.")

    # -------------------------------------------------------------
    # SALVAR RESULTADOS JSON PARA O DASHBOARD
    # -------------------------------------------------------------
    resultados = {
        "kpis": {
            "total_linhas": total_linhas,
            "receita_total": round(receita_total, 2),
            "total_particoes": len(particoes_criadas),
            "particoes": particoes_criadas
        },
        "pergunta_1_top_produtos": top10_produtos.to_dict(orient="records"),
        "pergunta_2_ticket_regional": ticket_regional.to_dict(orient="records"),
        "pergunta_3_crescimento_mom": crescimento_mensal.to_dict(orient="records")
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Respostas analíticas salvas em: {output_json}")
    print("=" * 75)

if __name__ == "__main__":
    resolver_desafios()
