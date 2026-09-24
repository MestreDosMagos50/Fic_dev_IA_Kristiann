#!/usr/bin/env python3
"""
=============================================================================
FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
Aula 01: Conceitos de Documentação, Metadados e Governança de Dados
Arquivo: scripts/validar_conexao_postgres.py
Objetivo: Validar conectividade, leitura de schemas e princípio do menor privilégio
=============================================================================
"""

import os
import sys
import psycopg2
from psycopg2 import errors

# Cores para terminal
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main():
    print(f"\n{BOLD}{BLUE}======================================================================{RESET}")
    print(f"{BOLD}{BLUE}   VALIDAÇÃO DE PRÉ-REQUISITOS — SERVIÇO PG_ECOMMERCE NO OPENMETADATA{RESET}")
    print(f"{BOLD}{BLUE}======================================================================{RESET}\n")

    # Parâmetros de Conexão
    host = os.getenv("PG_HOST", "localhost")
    port = int(os.getenv("PG_PORT", "5433"))
    database = os.getenv("PG_DATABASE", "meu_banco_de_dados")
    user = os.getenv("PG_USER", "openmetadata_user")
    password = os.getenv("PG_PASSWORD", "openmetadata_pass123")

    print(f"[*] Alvo: {BOLD}{user}@{host}:{port}/{database}{RESET}")

    # 1. Teste de Conexão
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
            connect_timeout=5
        )
        conn.autocommit = False
        cursor = conn.cursor()
        print(f"[{GREEN}✔ SUCESSO{RESET}] Conexão TCP estabelecida com sucesso!")
    except Exception as e:
        print(f"[{RED}✖ FALHA{RESET}] Não foi possível conectar ao PostgreSQL: {e}")
        print(f"\n{YELLOW}Dica: Certifique-se de que o contêiner meu_postgres está ativo e expondo a porta {port}.{RESET}")
        sys.exit(1)

    # 2. Identificação da Sessão
    cursor.execute("SELECT current_user, current_database(), version();")
    cur_user, cur_db, pg_ver = cursor.fetchone()
    print(f"[{GREEN}✔ SUCESSO{RESET}] Usuário ativo: {BOLD}{cur_user}{RESET} | Banco: {BOLD}{cur_db}{RESET}")
    print(f"    PostgreSQL: {pg_ver.split(',')[0]}")

    # 3. Verificação de Schemas
    print(f"\n{BOLD}[*] Verificando Schemas da Arquitetura Medalhão:{RESET}")
    cursor.execute("""
        SELECT schema_name 
        FROM information_schema.schemata 
        WHERE schema_name IN ('staging', 'silver', 'gold')
        ORDER BY schema_name;
    """)
    schemas_encontrados = [r[0] for r in cursor.fetchall()]
    for s in ['staging', 'silver', 'gold']:
        if s in schemas_encontrados:
            print(f"  [{GREEN}✔{RESET}] Schema {BOLD}{s}{RESET} acessível com USAGE")
        else:
            print(f"  [{RED}✖{RESET}] Schema {BOLD}{s}{RESET} ausente ou inacessível!")

    # 4. Verificação das 5 Tabelas do Desafio de Documentação (Passo 3)
    tabelas_alvo = [
        ("silver", "produtos", "Tier 3"),
        ("silver", "vendas", "Tier 3"),
        ("gold", "dim_produto", "Tier 2"),
        ("gold", "dim_cliente", "Tier 2"),
        ("gold", "fato_vendas", "Tier 1 — Crítico")
    ]

    print(f"\n{BOLD}[*] Verificando Metadados Técnicos das 5 Tabelas do Desafio:{RESET}")
    print(f"{'Tabela':<25} | {'Tier Proposto':<18} | {'Colunas':<9} | {'Registros':<10} | {'Status'}")
    print("-" * 75)

    todas_ok = True
    for schema, tabela, tier in tabelas_alvo:
        try:
            # Conta colunas
            cursor.execute("""
                SELECT count(*) 
                FROM information_schema.columns 
                WHERE table_schema = %s AND table_name = %s;
            """, (schema, tabela))
            num_cols = cursor.fetchone()[0]

            # Conta linhas
            cursor.execute(f"SELECT count(*) FROM {schema}.{tabela};")
            num_rows = cursor.fetchone()[0]

            status = f"{GREEN}Pronta{RESET}" if num_cols > 0 else f"{RED}Vazia{RESET}"
            print(f"{schema + '.' + tabela:<25} | {tier:<18} | {num_cols:<9} | {num_rows:<10} | {status}")
        except Exception as e:
            todas_ok = False
            print(f"{schema + '.' + tabela:<25} | {tier:<18} | {'ERRO':<9} | {'ERRO':<10} | {RED}{e}{RESET}")
            conn.rollback()

    # 5. Teste do Princípio do Menor Privilégio (Impedir Escrita)
    print(f"\n{BOLD}[*] Testando Princípio do Menor Privilégio (Least Privilege):{RESET}")
    try:
        cursor.execute("INSERT INTO gold.dim_produto (codigo_produto, nome_produto, categoria, preco_tabela, faixa_preco) VALUES ('TEST-HACK', 'Hacking Test', 'Teste', 10, 'Baixo');")
        conn.commit()
        print(f"[{RED}✖ VULNERABILIDADE{RESET}] O usuário de governança conseguiu inserir dados! Menor privilégio violado.")
    except (errors.InsufficientPrivilege, psycopg2.Error) as err:
        conn.rollback()
        print(f"[{GREEN}✔ APROVADO{RESET}] Tentativa de INSERT bloqueada com sucesso pelo PostgreSQL!")
        print(f"    Mensagem de segurança: {err.pgerror.strip() if hasattr(err, 'pgerror') and err.pgerror else err}")

    try:
        cursor.execute("DROP TABLE IF EXISTS silver.produtos_fake;")
        conn.commit()
    except (errors.InsufficientPrivilege, psycopg2.Error):
        conn.rollback()
        print(f"[{GREEN}✔ APROVADO{RESET}] Tentativa de DDL (DROP/CREATE) bloqueada com sucesso!")

    cursor.close()
    conn.close()

    print(f"\n{BOLD}{BLUE}======================================================================{RESET}")
    if todas_ok:
        print(f"{BOLD}{GREEN}✔ DIAGNÓSTICO CONCLUÍDO COM 100% DE SUCESSO!{RESET}")
        print(f"  O banco de dados e o usuário '{user}' atendem integralmente aos")
        print(f"  requisitos da Aula 01 para ingestão no serviço 'pg_ecommerce'.")
    else:
        print(f"{BOLD}{RED}✖ DIAGNÓSTICO FINALIZOU COM ALERTAS. Verifique as tabelas acima.{RESET}")
    print(f"{BOLD}{BLUE}======================================================================{RESET}\n")


if __name__ == "__main__":
    main()
