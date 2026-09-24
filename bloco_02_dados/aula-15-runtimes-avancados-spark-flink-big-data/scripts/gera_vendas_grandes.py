#!/usr/bin/env python3
# =============================================================================
# FIC Engenharia de Dados | Aula 04 (Módulo 2) / Aula 15
# Script: scripts/gera_vendas_grandes.py
# Objetivo: Gerar dataset de vendas massivo (CSV) para testes de Big Data
# =============================================================================

import os
import sys
import time
import argparse
import random
from datetime import datetime, timedelta

def gerar_dataset(num_linhas=1_000_000, output_path=None):
    if output_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(base_dir, "dados", "entrada", "vendas_grandes.csv")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("=" * 70)
    print("🚀 FIC ENGENHARIA DE DADOS — GERADOR DE VENDAS MASSIVAS (BIG DATA)")
    print(f"📊 Meta de linhas: {num_linhas:,}")
    print(f"📁 Arquivo de destino: {output_path}")
    print("=" * 70)

    produtos = [
        # (id_produto, nome, categoria, preco_base)
        ("PROD-001", "Notebook Gamer Dell G15", "Informática", 5200.00),
        ("PROD-002", "Monitor UltraWide 29 LG", "Informática", 1150.00),
        ("PROD-003", "Teclado Mecânico RGB Redragon", "Informática", 230.00),
        ("PROD-004", "Mouse Sem Fio Logitech MX Master", "Informática", 490.00),
        ("PROD-005", "Smartphone Samsung Galaxy S24", "Eletrônicos", 4800.00),
        ("PROD-006", "Smart TV 55 4K Crystal Samsung", "Eletrônicos", 2600.00),
        ("PROD-007", "Fone Bluetooth Sony WH-1000XM5", "Eletrônicos", 2100.00),
        ("PROD-008", "Cadeira Ergonômica Presidente", "Móveis", 980.00),
        ("PROD-009", "Mesa Ajustável de Escritório", "Móveis", 1450.00),
        ("PROD-010", "Geladeira Frost Free Brastemp", "Eletrodomésticos", 3700.00),
        ("PROD-011", "Micro-ondas 32L Electrolux", "Eletrodomésticos", 620.00),
        ("PROD-012", "Cafeteira Espresso Nespresso", "Eletrodomésticos", 420.00),
        ("PROD-013", "Bicicleta Aro 29 Mountain Bike", "Esporte", 1850.00),
        ("PROD-014", "Esteira Ergométrica Dobrável", "Esporte", 2900.00),
        ("PROD-015", "Kindle Paperwhite 16GB", "Livros & Cultura", 650.00),
    ]

    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    pesos_regioes = [0.45, 0.22, 0.18, 0.10, 0.05]  # Distribuição realista brasileira

    canais = ["E-commerce Web", "App Mobile", "Marketplace", "Loja Física"]
    pesos_canais = [0.40, 0.35, 0.15, 0.10]

    data_inicio = datetime(2026, 1, 1)
    dias_totais = 365

    start_time = time.time()
    linhas_geradas = 0
    chunk_size = 50_000

    header = "id_venda,data_venda,ano_mes,id_cliente,id_produto,produto,categoria,quantidade,preco_unitario,receita,regiao,canal_venda\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header)

        while linhas_geradas < num_linhas:
            linhas_bloco = []
            limite_atual = min(chunk_size, num_linhas - linhas_geradas)

            for i in range(limite_atual):
                id_venda = f"VEN-{linhas_geradas + i + 1:08d}"
                id_cliente = f"CLI-{random.randint(10000, 99999)}"
                dias_offset = random.randint(0, dias_totais - 1)
                dt = data_inicio + timedelta(days=dias_offset, seconds=random.randint(0, 86399))
                data_venda_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                ano_mes = dt.strftime("%Y-%m")

                prod = random.choice(produtos)
                id_prod, nome_prod, cat_prod, preco_base = prod

                # Variação de preço +/- 5%
                preco_unitario = round(preco_base * random.uniform(0.95, 1.05), 2)
                qtd = random.choices([1, 2, 3, 4, 5], weights=[0.65, 0.20, 0.08, 0.04, 0.03])[0]
                receita = round(preco_unitario * qtd, 2)

                regiao = random.choices(regioes, weights=pesos_regioes)[0]
                canal = random.choices(canais, weights=pesos_canais)[0]

                linhas_bloco.append(
                    f"{id_venda},{data_venda_str},{ano_mes},{id_cliente},{id_prod},{nome_prod},{cat_prod},{qtd},{preco_unitario:.2f},{receita:.2f},{regiao},{canal}\n"
                )

            f.writelines(linhas_bloco)
            linhas_geradas += limite_atual

            elapsed = time.time() - start_time
            taxa = linhas_geradas / elapsed if elapsed > 0 else 0
            progresso = (linhas_geradas / num_linhas) * 100
            print(f"\r⏳ Progresso: {progresso:5.1f}% | {linhas_geradas:,} linhas | {taxa:,.0f} linhas/s", end="", flush=True)

    print()
    total_time = time.time() - start_time
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)

    print("=" * 70)
    print(f"✅ CONCLUÍDO COM SUCESSO!")
    print(f"📦 Tamanho do arquivo CSV: {file_size_mb:.2f} MB")
    print(f"⏱️ Tempo total: {total_time:.2f} segundos")
    print(f"⚡ Velocidade média: {num_linhas / total_time:,.0f} linhas/s")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de Vendas Massivas para Big Data")
    parser.add_argument("--linhas", type=int, default=1_000_000, help="Número de linhas a gerar (padrão: 1.000.000)")
    parser.add_argument("--saida", type=str, default=None, help="Caminho do arquivo de saída")
    args = parser.parse_args()

    gerar_dataset(args.linhas, args.saida)
