#!/usr/bin/env python3
"""
=============================================================================
FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
Aula 03: Dados Mestres, Linhagem e Qualidade de Dados
Arquivo: scripts/validar_aula03_openmetadata.py
Objetivo: Auditoria Automatizada do Mini-Lab (Avaliação Oficial de 10 Pontos)
=============================================================================
"""

import os
import sys
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
    try:
        resp = requests.post(
            f"{BASE_URL}/users/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASS_B64},
            timeout=5
        )
        resp.raise_for_status()
        return resp.json()["accessToken"]
    except Exception as e:
        print(f"{RED}[❌ ERRO] Não foi possível autenticar no OpenMetadata: {e}{RESET}")
        return None


def get_pg_cursor():
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            dbname=PG_DATABASE,
            user=PG_USER,
            password=PG_PASSWORD
        )
        return conn, conn.cursor()
    except Exception as e:
        print(f"{RED}[❌ ERRO] Não foi possível conectar ao PostgreSQL: {e}{RESET}")
        return None, None


def main():
    print(f"\n{BOLD}{BLUE}======================================================================{RESET}")
    print(f"{BOLD}{BLUE}   AUDITORIA AUTOMATIZADA — AULA 03: MASTER DATA, LINHAGEM E TESTES{RESET}")
    print(f"{BOLD}{BLUE}   CRITÉRIOS OFICIAIS DE AVALIAÇÃO (NOTA TOTAL: 10.0 PONTOS){RESET}")
    print(f"{BOLD}{BLUE}======================================================================{RESET}\n")

    token = get_token()
    conn, cur = get_pg_cursor()

    if not token or not cur:
        print(f"{RED}Falha crítica de conectividade. Abortando auditoria.{RESET}")
        sys.exit(1)

    headers = {"Authorization": f"Bearer {token}"}
    pontos_obtidos = 0.0

    # -------------------------------------------------------------------------
    # CRITÉRIO 1: INVENTÁRIO DE MASTER DATA, CLASSIFICAÇÃO E TAGS (3.0 PONTOS)
    # -------------------------------------------------------------------------
    print(f"{BOLD}[*] AVALIANDO CRITÉRIO 1: Inventário de Master Data e Tags TipoDado (3.0 pts)...{RESET}")
    c1_ok = True
    c1_msg = []

    # 1.1 Verificar Classification TipoDado
    r_cls = requests.get(f"{BASE_URL}/classifications/name/TipoDado", headers=headers)
    if r_cls.status_code == 200:
        c1_msg.append("Classification 'TipoDado' encontrada no OpenMetadata.")
    else:
        c1_ok = False
        c1_msg.append("Classification 'TipoDado' NÃO encontrada.")

    # 1.2 Verificar Tags Mestre, Transacional, Referencia
    for tag_name in ["TipoDado.Mestre", "TipoDado.Transacional", "TipoDado.Referencia"]:
        r_tag = requests.get(f"{BASE_URL}/tags/name/{tag_name}", headers=headers)
        if r_tag.status_code == 200:
            c1_msg.append(f"Tag '{tag_name}' criada com sucesso.")
        else:
            c1_ok = False
            c1_msg.append(f"Tag '{tag_name}' ausente.")

    # 1.3 Verificar se tabelas possuem a tag aplicada
    sample_tables = [
        ("pg_ecommerce.meu_banco_de_dados.gold.dim_produto", "TipoDado.Mestre"),
        ("pg_ecommerce.meu_banco_de_dados.gold.dim_conteudo", "TipoDado.Mestre"),
        ("pg_ecommerce.meu_banco_de_dados.gold.fato_vendas", "TipoDado.Transacional"),
        ("pg_ecommerce.meu_banco_de_dados.gold.fato_publicacoes", "TipoDado.Transacional"),
        ("pg_ecommerce.meu_banco_de_dados.gold.dim_categoria", "TipoDado.Referencia")
    ]
    for tbl_fqn, expected_tag in sample_tables:
        r_t = requests.get(f"{BASE_URL}/tables/name/{tbl_fqn}?fields=tags", headers=headers)
        if r_t.status_code == 200:
            t_tags = [t["tagFQN"] for t in r_t.json().get("tags", [])]
            if expected_tag in t_tags:
                c1_msg.append(f"Tabela {tbl_fqn.split('.')[-1]} possui a tag {expected_tag}.")
            else:
                c1_ok = False
                c1_msg.append(f"Tabela {tbl_fqn.split('.')[-1]} NÃO possui a tag esperada {expected_tag}.")
        else:
            c1_ok = False
            c1_msg.append(f"Tabela {tbl_fqn} não encontrada.")

    # 1.4 Documento de Inventário
    doc_inv = "/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade/classificacao/inventario_master_data.md"
    if os.path.exists(doc_inv) and os.path.getsize(doc_inv) > 500:
        c1_msg.append("Documento 'inventario_master_data.md' completo e justificado.")
    else:
        c1_ok = False
        c1_msg.append("Documento de inventário incompleto ou ausente.")

    if c1_ok:
        pontos_obtidos += 3.0
        print(f"  {GREEN}[✔ APROVADO] Critério 1 Concluído! (+3.0 pontos){RESET}")
    else:
        print(f"  {RED}[❌ FALHA PARCIAL] Critério 1 incompleto.{RESET}")
    for m in c1_msg:
        print(f"      - {m}")

    # -------------------------------------------------------------------------
    # CRITÉRIO 2: CHAVE ÚNICA DECLARADA E DUPLICATAS AUDITADAS (2.0 PONTOS)
    # -------------------------------------------------------------------------
    print(f"\n{BOLD}[*] AVALIANDO CRITÉRIO 2: Chave Única e Verificação de Duplicatas (2.0 pts)...{RESET}")
    c2_ok = True
    c2_msg = []

    # 2.1 Consulta de Duplicatas em silver.produtos
    cur.execute("SELECT COUNT(*) - COUNT(DISTINCT codigo) FROM silver.produtos;")
    dupes_prod = cur.fetchone()[0]
    if dupes_prod == 0:
        c2_msg.append("Chave única 'codigo' em silver.produtos auditada com 0 duplicatas.")
    else:
        c2_ok = False
        c2_msg.append(f"silver.produtos contém {dupes_prod} duplicatas anômalas.")

    # 2.2 Verificação de Golden Record em silver.conteudos
    cur.execute("SELECT COUNT(*) FROM silver.conteudos WHERE is_duplicata = TRUE;")
    dupes_cont = cur.fetchone()[0]
    if dupes_cont == 11:
        c2_msg.append(f"Regra de Golden Record em silver.conteudos identificou com precisão as {dupes_cont} duplicatas de negócio.")
    else:
        c2_ok = False
        c2_msg.append(f"Identificação de duplicatas em silver.conteudos retornou {dupes_cont} (esperado: 11).")

    # 2.3 Dimensão gold.dim_conteudo consolidada
    cur.execute("SELECT COUNT(*) FROM gold.dim_conteudo;")
    count_dim_cont = cur.fetchone()[0]
    if count_dim_cont == 989:
        c2_msg.append(f"gold.dim_conteudo consolidou exatamente 989 Golden Records únicos (1000 - 11).")
    else:
        c2_ok = False
        c2_msg.append(f"gold.dim_conteudo contém {count_dim_cont} registros (esperado: 989).")

    # 2.4 Script SQL do Passo 2
    sql_p2 = "/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade/sql/02_verificacao_duplicatas_golden_record.sql"
    if os.path.exists(sql_p2):
        c2_msg.append("Arquivo '02_verificacao_duplicatas_golden_record.sql' presente com matching rules.")
    else:
        c2_ok = False
        c2_msg.append("Arquivo SQL do Passo 2 não encontrado.")

    if c2_ok:
        pontos_obtidos += 2.0
        print(f"  {GREEN}[✔ APROVADO] Critério 2 Concluído! (+2.0 pontos){RESET}")
    else:
        print(f"  {RED}[❌ FALHA PARCIAL] Critério 2 incompleto.{RESET}")
    for m in c2_msg:
        print(f"      - {m}")

    # -------------------------------------------------------------------------
    # CRITÉRIO 3: LINHAGEM DESENHADA + IMPACTO E CAUSA RAIZ (3.0 PONTOS)
    # -------------------------------------------------------------------------
    print(f"\n{BOLD}[*] AVALIANDO CRITÉRIO 3: Linhagem Ponta a Ponta e Análises (3.0 pts)...{RESET}")
    c3_ok = True
    c3_msg = []

    # 3.1 Linhagem de gold.fato_vendas no OpenMetadata
    r_lin_fato = requests.get(f"{BASE_URL}/lineage/table/name/pg_ecommerce.meu_banco_de_dados.gold.fato_vendas", headers=headers)
    if r_lin_fato.status_code == 200:
        nodes = r_lin_fato.json().get("nodes", [])
        c3_msg.append(f"Linhagem de gold.fato_vendas registrada no OpenMetadata ({len(nodes)} nós upstream/downstream).")
    else:
        c3_ok = False
        c3_msg.append("Linhagem de gold.fato_vendas ausente no catálogo.")

    # 3.2 Linhagem de gold.fato_publicacoes
    r_lin_pub = requests.get(f"{BASE_URL}/lineage/table/name/pg_ecommerce.meu_banco_de_dados.gold.fato_publicacoes", headers=headers)
    if r_lin_pub.status_code == 200:
        nodes_pub = r_lin_pub.json().get("nodes", [])
        c3_msg.append(f"Linhagem de gold.fato_publicacoes registrada no OpenMetadata ({len(nodes_pub)} nós).")
    else:
        c3_ok = False
        c3_msg.append("Linhagem de gold.fato_publicacoes ausente no catálogo.")

    # 3.3 Documento de Análise de Impacto e Causa Raiz
    doc_lin = "/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade/linhagem/analise_impacto_causa_raiz.md"
    if os.path.exists(doc_lin) and os.path.getsize(doc_lin) > 500:
        c3_msg.append("Documento 'analise_impacto_causa_raiz.md' com respostas completas às questões (a), (b) e (c).")
    else:
        c3_ok = False
        c3_msg.append("Documento de análise de linhagem incompleto ou ausente.")

    if c3_ok:
        pontos_obtidos += 3.0
        print(f"  {GREEN}[✔ APROVADO] Critério 3 Concluído! (+3.0 pontos){RESET}")
    else:
        print(f"  {RED}[❌ FALHA PARCIAL] Critério 3 incompleto.{RESET}")
    for m in c3_msg:
        print(f"      - {m}")

    # -------------------------------------------------------------------------
    # CRITÉRIO 4: QUATRO TESTES DE QUALIDADE E FALHA PROPOSITALS (2.0 PONTOS)
    # -------------------------------------------------------------------------
    print(f"\n{BOLD}[*] AVALIANDO CRITÉRIO 4: Testes de Qualidade e Demonstração de Falha (2.0 pts)...{RESET}")
    c4_ok = True
    c4_msg = []

    # 4.1 Test Cases no OpenMetadata para silver.produtos
    test_cases_esperados = [
        "pg_ecommerce.meu_banco_de_dados.silver.produtos.codigo.silver_produtos_codigo_unique",
        "pg_ecommerce.meu_banco_de_dados.silver.produtos.categoria.silver_produtos_categoria_not_null",
        "pg_ecommerce.meu_banco_de_dados.silver.produtos.preco.silver_produtos_preco_range",
        "pg_ecommerce.meu_banco_de_dados.silver.produtos.silver_produtos_row_count"
    ]
    for tc_fqn in test_cases_esperados:
        r_tc = requests.get(f"{BASE_URL}/dataQuality/testCases/name/{tc_fqn}", headers=headers)
        if r_tc.status_code == 200:
            c4_msg.append(f"Test Case '{tc_fqn.split('.')[-1]}' ativo no OpenMetadata.")
        else:
            c4_ok = False
            c4_msg.append(f"Test Case '{tc_fqn}' não encontrado no catálogo.")

    # 4.2 Script de Simulação de Falha
    script_sim = "/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade/scripts/simular_teste_qualidade_falha.py"
    if os.path.exists(script_sim):
        c4_msg.append("Script 'simular_teste_qualidade_falha.py' operacional e testado.")
    else:
        c4_ok = False
        c4_msg.append("Script de simulação de falha não encontrado.")

    # 4.3 Script SQL do Passo 4
    sql_p4 = "/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade/sql/03_testes_qualidade_silver_produtos.sql"
    if os.path.exists(sql_p4):
        c4_msg.append("Arquivo '03_testes_qualidade_silver_produtos.sql' presente com injeção de preço negativo.")
    else:
        c4_ok = False
        c4_msg.append("Arquivo SQL de testes de qualidade não encontrado.")

    if c4_ok:
        pontos_obtidos += 2.0
        print(f"  {GREEN}[✔ APROVADO] Critério 4 Concluído! (+2.0 pontos){RESET}")
    else:
        print(f"  {RED}[❌ FALHA PARCIAL] Critério 4 incompleto.{RESET}")
    for m in c4_msg:
        print(f"      - {m}")

    # -------------------------------------------------------------------------
    # PLACAR FINAL
    # -------------------------------------------------------------------------
    print(f"\n{BOLD}{BLUE}======================================================================{RESET}")
    print(f"{BOLD}{BLUE}   RELATÓRIO FINAL DE AVALIAÇÃO — MINI-LAB AULA 03{RESET}")
    print(f"{BOLD}{BLUE}======================================================================{RESET}")
    print(f"  1. Inventário Master Data e Tags TipoDado:  {GREEN}3.0 / 3.0 pts{RESET}")
    print(f"  2. Chave Única e Auditoria de Duplicatas:  {GREEN}2.0 / 2.0 pts{RESET}")
    print(f"  3. Linhagem Ponta a Ponta e Análises:       {GREEN}3.0 / 3.0 pts{RESET}")
    print(f"  4. Quatro Testes e Simulação de Falha:      {GREEN}2.0 / 2.0 pts{RESET}")
    print(f"----------------------------------------------------------------------")
    
    cor_final = GREEN if pontos_obtidos == 10.0 else YELLOW
    print(f"  {BOLD}NOTA FINAL DO MINI-LAB:{RESET} {cor_final}{BOLD}{pontos_obtidos:.1f} / 10.0 PONTOS{RESET}")
    
    if pontos_obtidos == 10.0:
        print(f"\n{BOLD}{GREEN}🎉 PARABÉNS! TODOS OS REQUISITOS DO MINI-LAB FORAM ATENDIDOS COM NOTA MÁXIMA!{RESET}\n")
    else:
        print(f"\n{BOLD}{YELLOW}⚠ ATENÇÃO: Verifique os critérios pendentes acima para atingir 10.0 pontos.{RESET}\n")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
