#!/usr/bin/env python3
"""
=============================================================================
FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
Aula 03: Dados Mestres, Linhagem e Qualidade de Dados
Arquivo: scripts/carregar_conteudos_postgres.py
Objetivo: Ingestão e pipeline completo do dataset conteudos.csv:
          CSV (Bronze) -> staging.conteudos -> silver.conteudos (MDM/Golden Record)
          -> gold.dim_conteudo, gold.dim_autor, gold.dim_categoria, gold.fato_publicacoes
=============================================================================
"""

import os
import csv
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5433"))
PG_DATABASE = os.getenv("PG_DATABASE", "meu_banco_de_dados")
PG_USER = os.getenv("PG_USER", "vinycius")
PG_PASSWORD = os.getenv("PG_PASSWORD", "120521Batata@")

CSV_PATH = "/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade/dados/conteudos.csv"
SQL_DDL_PATH = "/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade/sql/00_prepara_tabelas_conteudos.sql"


def get_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_USER,
        password=PG_PASSWORD
    )


def execute_ddl(cursor):
    print("\n[*] 1. Executando DDL das camadas staging, silver e gold...")
    with open(SQL_DDL_PATH, "r", encoding="utf-8") as f:
        ddl_sql = f.read()
    cursor.execute(ddl_sql)
    print("  [✔] Tabelas e permissões criadas com sucesso.")


def carregar_staging(cursor):
    print("\n[*] 2. Ingestão Bronze -> staging.conteudos (1000 registros brutos)...")
    cursor.execute("TRUNCATE TABLE staging.conteudos;")
    
    rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append((
                int(row["conteudo_id"]),
                row["titulo"].strip(),
                row["tipo"].strip(),
                row["categoria"].strip(),
                row["nivel"].strip(),
                int(row["carga_horaria_min"]),
                row["data_publicacao"].strip(),
                row["descricao"].strip(),
                row["autor"].strip()
            ))

    insert_sql = """
        INSERT INTO staging.conteudos (
            conteudo_id, titulo, tipo, categoria, nivel, 
            carga_horaria_min, data_publicacao, descricao, autor
        ) VALUES %s;
    """
    execute_values(cursor, insert_sql, rows)
    print(f"  [✔] {len(rows)} registros inseridos em staging.conteudos.")
    return rows


def processar_silver_mdm(cursor):
    print("\n[*] 3. Transformação & MDM Staging -> silver.conteudos...")
    print("  [*] Aplicando regras de correspondência (Matching por Título Normalizado + Autor)...")
    
    cursor.execute("TRUNCATE TABLE silver.conteudos;")
    
    # Query inteligente que detecta duplicatas por (titulo, autor)
    # e define o primeiro registro (menor conteudo_id / menor data) como Golden Record
    sql_silver = """
        WITH cte_classificacao AS (
            SELECT 
                conteudo_id,
                titulo,
                tipo,
                categoria,
                nivel,
                carga_horaria_min,
                data_publicacao,
                descricao,
                autor,
                ROW_NUMBER() OVER (
                    PARTITION BY LOWER(TRIM(titulo)), LOWER(TRIM(autor)) 
                    ORDER BY data_publicacao ASC, conteudo_id ASC
                ) as rn,
                FIRST_VALUE(conteudo_id) OVER (
                    PARTITION BY LOWER(TRIM(titulo)), LOWER(TRIM(autor)) 
                    ORDER BY data_publicacao ASC, conteudo_id ASC
                ) as golden_id
            FROM staging.conteudos
        )
        INSERT INTO silver.conteudos (
            conteudo_id, titulo, tipo, categoria, nivel,
            carga_horaria_min, data_publicacao, descricao, autor,
            is_duplicata, golden_record_id
        )
        SELECT 
            conteudo_id,
            titulo,
            tipo,
            categoria,
            nivel,
            carga_horaria_min,
            data_publicacao,
            descricao,
            autor,
            CASE WHEN rn > 1 THEN TRUE ELSE FALSE END as is_duplicata,
            golden_id
        FROM cte_classificacao;
    """
    cursor.execute(sql_silver)
    
    cursor.execute("SELECT count(*), count(*) FILTER (WHERE is_duplicata = TRUE) FROM silver.conteudos;")
    total, duplicatas = cursor.fetchone()
    print(f"  [✔] {total} registros processados em silver.conteudos.")
    print(f"  [!] {duplicatas} registros classificados como duplicatas de negócio (re-publicações/versões).")


def popular_gold_dimensional(cursor):
    print("\n[*] 4. Carga Analítica Silver -> Camada Gold (Star Schema)...")
    
    # 4.1 Dimensão Categoria (Referência)
    cursor.execute("TRUNCATE TABLE gold.fato_publicacoes CASCADE;")
    cursor.execute("TRUNCATE TABLE gold.dim_conteudo CASCADE;")
    cursor.execute("TRUNCATE TABLE gold.dim_autor CASCADE;")
    cursor.execute("TRUNCATE TABLE gold.dim_categoria CASCADE;")
    
    sql_categoria = """
        INSERT INTO gold.dim_categoria (nome_categoria, macro_area, total_titulos)
        SELECT 
            categoria,
            CASE 
                WHEN categoria IN ('Engenharia de Dados', 'DevOps & Cloud', 'Banco de Dados') THEN 'Infraestrutura & Engenharia'
                WHEN categoria IN ('Business Intelligence', 'Ciência de Dados', 'Inteligência Artificial') THEN 'Analytics & Inteligência Artificial'
                ELSE 'Engenharia de Software & Governança'
            END as macro_area,
            COUNT(DISTINCT conteudo_id)
        FROM silver.conteudos
        GROUP BY categoria
        ORDER BY categoria;
    """
    cursor.execute(sql_categoria)
    print("  [✔] Dimensão gold.dim_categoria populada (8 categorias canônicas).")

    # 4.2 Dimensão Autor (Master Data)
    sql_autor = """
        INSERT INTO gold.dim_autor (nome_autor, titulacao, nome_limpo, total_conteudos, total_horas, categoria_principal)
        SELECT 
            autor,
            CASE 
                WHEN autor LIKE 'Profa.%' THEN 'Professora'
                WHEN autor LIKE 'Prof.%' THEN 'Professor'
                WHEN autor LIKE 'Dra.%' THEN 'Doutora'
                WHEN autor LIKE 'Dr.%' THEN 'Doutor'
                WHEN autor LIKE 'Eng.%' THEN 'Engenheiro(a)'
                ELSE 'Especialista'
            END as titulacao,
            REGEXP_REPLACE(autor, '^(Profa\\.|Prof\\.|Dra\\.|Dr\\.|Eng\\.)\\s*', '') as nome_limpo,
            COUNT(*) as total_conteudos,
            ROUND(SUM(carga_horaria_min)::numeric / 60, 2) as total_horas,
            MODE() WITHIN GROUP (ORDER BY categoria) as categoria_principal
        FROM silver.conteudos
        GROUP BY autor
        ORDER BY autor;
    """
    cursor.execute(sql_autor)
    print("  [✔] Dimensão gold.dim_autor populada (20 autores cadastrados como Master Data).")

    # 4.3 Dimensão Conteúdo (Master Data / Golden Record)
    sql_conteudo = """
        INSERT INTO gold.dim_conteudo (
            conteudo_id, titulo, tipo, categoria, nivel, 
            carga_horaria_min, carga_horaria_horas, autor, 
            data_primeira_publicacao, versoes_identificadas
        )
        SELECT 
            s.golden_record_id,
            s.titulo,
            s.tipo,
            s.categoria,
            s.nivel,
            s.carga_horaria_min,
            ROUND(s.carga_horaria_min::numeric / 60, 2),
            s.autor,
            s.data_publicacao,
            sub.qtd_versoes
        FROM silver.conteudos s
        JOIN (
            SELECT golden_record_id, count(*) as qtd_versoes
            FROM silver.conteudos
            GROUP BY golden_record_id
        ) sub ON sub.golden_record_id = s.golden_record_id
        WHERE s.is_duplicata = FALSE
        ORDER BY s.golden_record_id;
    """
    cursor.execute(sql_conteudo)
    cursor.execute("SELECT count(*) FROM gold.dim_conteudo;")
    total_dim_cont = cursor.fetchone()[0]
    print(f"  [✔] Dimensão gold.dim_conteudo populada ({total_dim_cont} Golden Records consolidados).")

    # 4.4 Fato Publicações (Transacional)
    sql_fato = """
        INSERT INTO gold.fato_publicacoes (
            conteudo_id, sk_conteudo, sk_autor, sk_categoria, 
            tipo, nivel, data_publicacao, ano_publicacao, mes_publicacao, 
            carga_horaria_min, carga_horaria_horas
        )
        SELECT 
            s.conteudo_id,
            dc.sk_conteudo,
            da.sk_autor,
            dcat.sk_categoria,
            s.tipo,
            s.nivel,
            s.data_publicacao,
            EXTRACT(YEAR FROM s.data_publicacao)::int,
            EXTRACT(MONTH FROM s.data_publicacao)::int,
            s.carga_horaria_min,
            ROUND(s.carga_horaria_min::numeric / 60, 2)
        FROM silver.conteudos s
        JOIN gold.dim_conteudo dc ON dc.conteudo_id = s.golden_record_id
        JOIN gold.dim_autor da ON da.nome_autor = s.autor
        JOIN gold.dim_categoria dcat ON dcat.nome_categoria = s.categoria
        ORDER BY s.conteudo_id;
    """
    cursor.execute(sql_fato)
    cursor.execute("SELECT count(*) FROM gold.fato_publicacoes;")
    total_fato = cursor.fetchone()[0]
    print(f"  [✔] Tabela Fato gold.fato_publicacoes populada ({total_fato} eventos de publicação).")


def main():
    print("======================================================================")
    print("   ETL & MDM PIPELINE — CONTEUDOS.CSV (BRONZE -> STAGING -> SILVER -> GOLD)")
    print("======================================================================")
    
    conn = get_connection()
    conn.autocommit = False
    try:
        with conn.cursor() as cur:
            execute_ddl(cur)
            carregar_staging(cur)
            processar_silver_mdm(cur)
            popular_gold_dimensional(cur)
            conn.commit()
            print("\n======================================================================")
            print("✔ PIPELINE DE CONTEÚDOS EXECUTADO COM SUCESSO NO POSTGRESQL!")
            print("======================================================================\n")
    except Exception as e:
        conn.rollback()
        print(f"\n[❌ ERRO] Falha no pipeline: {e}")
        raise e
    finally:
        conn.close()


if __name__ == "__main__":
    main()
