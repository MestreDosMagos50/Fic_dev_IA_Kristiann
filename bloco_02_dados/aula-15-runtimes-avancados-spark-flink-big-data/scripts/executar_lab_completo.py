#!/usr/bin/env python3
# =============================================================================
# FIC Engenharia de Dados | Aula 04 (Módulo 2) / Aula 15
# Script: scripts/executar_lab_completo.py
# Objetivo: Orquestrador mestre para executar todos os passos do mini-lab Big Data
# =============================================================================

import os
import sys
import time
import subprocess

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scripts_dir = os.path.join(base_dir, "scripts")

    print("=" * 80)
    print("🌟 ORQUESTRADOR COMPLETO DA AULA 15: RUNTIMES AVANÇADOS & BIG DATA")
    print("=" * 80)

    passos = [
        ("Passo 1: Geração do Dataset Massivo (~1M linhas)", "gera_vendas_grandes.py", ["--linhas", "1000000"]),
        ("Passo 2: Benchmark CSV vs. Parquet (Conversão e Performance)", "benchmark_csv_vs_parquet.py", []),
        ("Passo 3: Comparação de Runtimes (Hop Local vs. Spark Local[*])", "executar_hop_runtimes.py", []),
        ("Passo 4: Desafio de Negócios e Exportação Particionada por Mês", "responder_desafios_negocio.py", []),
        ("Passo 5: Geração do Dashboard Web Interativo", "gerar_dashboard.py", [])
    ]

    t0_geral = time.time()

    for idx, (nome, script_name, args) in enumerate(passos, 1):
        print(f"\n▶️ [{idx}/5] {nome}...")
        script_path = os.path.join(scripts_dir, script_name)
        cmd = [sys.executable, script_path] + args
        t0 = time.time()
        res = subprocess.run(cmd, cwd=base_dir)
        if res.returncode != 0:
            print(f"❌ Erro ao executar {script_name}!")
            sys.exit(res.returncode)
        print(f"✔️ Concluído em {time.time() - t0:.2f}s")

    print("\n" + "=" * 80)
    print(f"🎉 TODO O LABORATÓRIO DA AULA 15 FOI EXECUTADO COM SUCESSO EM {time.time() - t0_geral:.2f}s!")
    print(f"🌐 Abra o arquivo index.html no navegador para visualizar o Dashboard Completo.")
    print("=" * 80)

if __name__ == "__main__":
    main()
