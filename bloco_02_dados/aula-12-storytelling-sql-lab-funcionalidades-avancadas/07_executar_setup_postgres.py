#!/usr/bin/env python3
"""
FIC DEV IA – Engenharia de Dados | Aula 12
Script de Automação: Executar Carga no PostgreSQL para o Superset
"""

import os
import sys
import subprocess

def carregar_via_docker():
    """Tenta carregar o script SQL via contêiner Docker data_postgres ou meu_postgres."""
    sql_file = os.path.join(os.path.dirname(__file__), "01_preparar_dados_vendas_detalhe.sql")
    if not os.path.exists(sql_file):
        print(f"Arquivo não encontrado: {sql_file}")
        return False

    with open(sql_file, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Tenta contêiner data_postgres primeiro, depois meu_postgres
    for container in ["data_postgres", "meu_postgres"]:
        try:
            print(f"Tentando executar no contêiner Docker '{container}'...")
            cmd = ["docker", "exec", "-i", container, "psql", "-U", "superset_user", "-d", "superset_data"]
            proc = subprocess.run(cmd, input=sql_content, text=True, capture_output=True, timeout=10)
            if proc.returncode == 0:
                print(f"✅ Sucesso executando no contêiner {container}!")
                print(proc.stdout)
                return True
            else:
                print(f"⚠️ Falha no contêiner {container}: {proc.stderr.strip()}")
        except Exception as e:
            print(f"Erro ao tentar Docker ({container}): {e}")

    return False

def carregar_via_psql_local():
    """Tenta executar via comando psql local."""
    sql_file = os.path.join(os.path.dirname(__file__), "01_preparar_dados_vendas_detalhe.sql")
    try:
        print("Tentando via psql local na porta 5432...")
        env = os.environ.copy()
        env["PGPASSWORD"] = "superset_password"
        cmd = ["psql", "-h", "localhost", "-p", "5432", "-U", "superset_user", "-d", "superset_data", "-f", sql_file]
        proc = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=10)
        if proc.returncode == 0:
            print("✅ Sucesso executando via psql local!")
            print(proc.stdout)
            return True
        else:
            print(f"⚠️ psql local porta 5432: {proc.stderr.strip()}")
    except Exception as e:
        print(f"Erro psql: {e}")

    return False

if __name__ == "__main__":
    print("=== Inicializando Configuração das Tabelas da Aula 12 ===")
    if carregar_via_docker() or carregar_via_psql_local():
        print("\n🎉 Dados de 'vendas_detalhe' e 'produtos_master' criados e carregados com sucesso!")
        print("Agora você pode acessar o Apache Superset (http://localhost:8088) e utilizar o SQL Lab.")
    else:
        print("\nℹ️ Não foi possível conectar automaticamente ao banco.")
        print("Você pode rodar manualmente:")
        print("  psql -h localhost -U superset_user -d superset_data -f 01_preparar_dados_vendas_detalhe.sql")
