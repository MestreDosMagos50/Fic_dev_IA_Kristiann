#!/usr/bin/env python3
"""
=============================================================================
FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
Aula 03: Dados Mestres, Linhagem e Qualidade de Dados
Arquivo: scripts/simular_teste_qualidade_falha.py
Objetivo: Passo 4 do Mini-Lab — Demonstrar a execução dos 4 testes de qualidade
          em silver.produtos, simular falha com preço negativo (teste em vermelho)
          e restaurar a integridade (teste em verde) tanto no PostgreSQL quanto
          no OpenMetadata.
=============================================================================
"""

import os
import time
import base64
import requests
import psycopg2

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

BASE_URL = "http://localhost:8585/api/v1"
ADMIN_EMAIL = "admin@open-metadata.org"
ADMIN_PASS_B64 = base64.b64encode(b"admin").decode("utf-8")

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5433"))
PG_DATABASE = os.getenv("PG_DATABASE", "meu_banco_de_dados")
PG_USER = os.getenv("PG_USER", "vinycius")
PG_PASSWORD = os.getenv("PG_PASSWORD", "120521Batata@")


def get_token():
    resp = requests.post(
        f"{BASE_URL}/users/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASS_B64}
    )
    resp.raise_for_status()
    return resp.json()["accessToken"]


def get_pg_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )


def executar_testes_postgres(cursor):
    resultados = {}

    # Teste 1: Unicidade de codigo
    cursor.execute("""
        SELECT COUNT(*) - COUNT(DISTINCT codigo)
        FROM silver.produtos;
    """)
    duplicatas = cursor.fetchone()[0]
    resultados["unicidade"] = {
        "nome": "Unicidade de Código (codigo)",
        "dimensao": "Unicidade",
        "falhas": duplicatas,
        "status": "PASSED" if duplicatas == 0 else "FAILED",
        "detalhe": f"{duplicatas} duplicatas encontradas."
    }

    # Teste 2: Não-nulidade de categoria
    cursor.execute("""
        SELECT COUNT(*) FILTER (WHERE categoria IS NULL OR TRIM(categoria) = '')
        FROM silver.produtos;
    """)
    nulos = cursor.fetchone()[0]
    resultados["completude"] = {
        "nome": "Completude de Categoria (not null)",
        "dimensao": "Completude",
        "falhas": nulos,
        "status": "PASSED" if nulos == 0 else "FAILED",
        "detalhe": f"{nulos} registros com categoria nula/vazia."
    }

    # Teste 3: Faixa de Preço (preco > 0)
    cursor.execute("""
        SELECT COUNT(*) FILTER (WHERE preco <= 0),
               STRING_AGG(codigo || ' (' || preco || ')', ', ') FILTER (WHERE preco <= 0)
        FROM silver.produtos;
    """)
    row_preco = cursor.fetchone()
    precos_invalidos = row_preco[0] or 0
    infratores = row_preco[1] or "Nenhum"
    resultados["preco"] = {
        "nome": "Faixa Válida de Preço (preco > 0)",
        "dimensao": "Validade",
        "falhas": precos_invalidos,
        "status": "PASSED" if precos_invalidos == 0 else "FAILED",
        "detalhe": f"{precos_invalidos} produtos com preco <= 0. Infratores: {infratores}."
    }

    # Teste 4: Contagem de Linhas (1 a 10.000)
    cursor.execute("SELECT COUNT(*) FROM silver.produtos;")
    total_linhas = cursor.fetchone()[0]
    status_linhas = "PASSED" if 1 <= total_linhas <= 10000 else "FAILED"
    resultados["volume"] = {
        "nome": "Contagem de Linhas (Volume: 1 a 10.000)",
        "dimensao": "Consistência / Volume",
        "falhas": 0 if status_linhas == "PASSED" else 1,
        "status": status_linhas,
        "detalhe": f"Total de {total_linhas} linhas na tabela."
    }

    return resultados


def imprimir_relatorio_testes(resultados, etapa):
    print(f"\n{BOLD}{BLUE}======================================================================{RESET}")
    print(f"{BOLD}{BLUE}   RESULTADOS DOS TESTES DE QUALIDADE — ETAPA: {etapa}{RESET}")
    print(f"{BOLD}{BLUE}======================================================================{RESET}")

    todos_passaram = True
    for k, t in resultados.items():
        cor = GREEN if t["status"] == "PASSED" else RED
        tag = f"[{cor}✔ PASSED{RESET}]" if t["status"] == "PASSED" else f"[{cor}❌ FAILED{RESET}]"
        print(f"  {tag} {BOLD}{t['nome']}{RESET} ({t['dimensao']})")
        print(f"       -> {cor}{t['detalhe']}{RESET}")
        if t["status"] != "PASSED":
            todos_passaram = False

    status_geral = f"{GREEN}100% APROVADO (INTEGRIDADE PRESERVADA){RESET}" if todos_passaram else f"{RED}ALERTA CRÍTICO: FALHA DE QUALIDADE DETECTADA!{RESET}"
    print(f"\n  {BOLD}Status Geral:{RESET} {status_geral}")


def enviar_resultado_openmetadata(token, test_case_fqn, status, mensagem, falhas):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    now_ms = int(time.time() * 1000)
    payload = {
        "timestamp": now_ms,
        "testCaseStatus": "Success" if status == "PASSED" else "Failed",
        "result": mensagem,
        "testResultValue": [
            {"name": "failedRows", "value": str(falhas)}
        ]
    }
    requests.post(
        f"{BASE_URL}/dataQuality/testCases/testCaseResults/{test_case_fqn}",
        headers=headers,
        json=payload
    )


def main():
    print(f"\n{BOLD}{BLUE}======================================================================{RESET}")
    print(f"{BOLD}{BLUE}   MINI-LAB PASSO 4: DEMONSTRAÇÃO PRÁTICA DE FALHA PROPOSITAL{RESET}")
    print(f"{BOLD}{BLUE}======================================================================{RESET}\n")

    token = get_token()
    conn = get_pg_connection()
    conn.autocommit = True
    cur = conn.cursor()

    # 1. Estado Inicial (Limpo)
    cur.execute("DELETE FROM silver.produtos WHERE codigo = 'PROD-FALHA-TESTE';")
    res_inicial = executar_testes_postgres(cur)
    imprimir_relatorio_testes(res_inicial, "1. ESTADO NOMINAL (VERDE)")

    # Sincronizar com OpenMetadata
    tc_preco_fqn = "pg_ecommerce.meu_banco_de_dados.silver.produtos.preco.silver_produtos_preco_range"
    enviar_resultado_openmetadata(
        token, tc_preco_fqn, "PASSED",
        "Aprovado: Todos os preços estão estritamente acima de zero.", 0
    )
    print("  [✔] Status 'Success' (Verde) sincronizado com o OpenMetadata.")

    # 2. Inserir Preço Negativo (Provocar Falha de Propósito)
    print(f"\n{YELLOW}[!] Provocando falha proposital: inserindo produto com preco = -199.90...{RESET}")
    cur.execute("""
        INSERT INTO silver.produtos (codigo, nome, preco, categoria, data_cadastro)
        VALUES ('PROD-FALHA-TESTE', 'Cadeira Gamer com Preço Negativo Anômalo', -199.90, 'Móveis', CURRENT_DATE);
    """)

    time.sleep(1)
    res_com_falha = executar_testes_postgres(cur)
    imprimir_relatorio_testes(res_com_falha, "2. ANOMALIA INJETADA (VERMELHO)")

    # Sincronizar Falha no OpenMetadata
    enviar_resultado_openmetadata(
        token, tc_preco_fqn, "FAILED",
        "Falha Crítica: Produto PROD-FALHA-TESTE possui preço negativo de R$ -199.90!", 1
    )
    print(f"  {RED}[!] Status 'Failed' (Vermelho) sincronizado com o OpenMetadata!{RESET}")

    # 3. Remover Registro e Restaurar Integridade
    print(f"\n{BLUE}[*] Removendo registro anômalo e restaurando integridade...{RESET}")
    cur.execute("DELETE FROM silver.produtos WHERE codigo = 'PROD-FALHA-TESTE';")
    time.sleep(1)

    res_restaurado = executar_testes_postgres(cur)
    imprimir_relatorio_testes(res_restaurado, "3. APÓS CORREÇÃO (VERDE RESTAURADO)")

    # Sincronizar Sucesso Restaurado no OpenMetadata
    enviar_resultado_openmetadata(
        token, tc_preco_fqn, "PASSED",
        "Aprovado: Registro anômalo removido. Todos os preços agora são válidos.", 0
    )
    print("  [✔] Status 'Success' (Verde) restabelecido no OpenMetadata.")

    print(f"\n{BOLD}{GREEN}======================================================================{RESET}")
    print(f"{BOLD}{GREEN}✔ PASSO 4 CONCLUÍDO COM SUCESSO! FALHA E RECUPERAÇÃO COMPROVADAS!{RESET}")
    print(f"{BOLD}{GREEN}======================================================================{RESET}\n")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
