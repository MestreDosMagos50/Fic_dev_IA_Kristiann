"""
04_staging_incremental_idempotencia.py — Conceitos Operacionais Essenciais de Pipelines
Módulo 2 / Aula 01 — FIC Engenharia de Dados

Tópicos Fundamentais da Apostila:
1. Staging Area: Área intermediária de pouso dos dados para auditoria e desacoplamento da fonte.
2. Carga Completa vs Carga Incremental:
   - Completa: Limpa e recarrega tudo (simples, mas não escala para grandes volumes).
   - Incremental: Processa apenas dados novos ou alterados (via timestamp ou Change Data Capture - CDC).
3. Idempotência:
   - Capacidade do pipeline produzir exatamente o mesmo estado mesmo se executado 2, 5 ou 10 vezes seguidas.
   - Essencial para tolerância a falhas: se a execução quebrar na metade, basta rodar novamente sem duplicar dados.
"""

import sqlite3
import pandas as pd
from datetime import datetime

def demonstrar_staging_area(conn: sqlite3.Connection):
    """
    1. STAGING AREA:
    Área intermediária onde os dados extraídos 'pousam' antes da transformação.
    Permite auditar o que foi extraído e reprocessar sem re-extrair da fonte original.
    """
    print("\n" + "=" * 70)
    print("1. CONCEITO: STAGING AREA")
    print("=" * 70)
    
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS staging_pedidos (
            id_transacao TEXT,
            cliente_raw TEXT,
            valor_raw TEXT,
            data_extracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Ingestão bruta na staging (sem limpeza prévia)
    pedidos_fonte = [
        ("T101", "  joao da silva ", "R$ 150,00"),
        ("T102", "maria oliveira", "R$ 2.400,50"),
    ]
    cur.executemany("INSERT INTO staging_pedidos (id_transacao, cliente_raw, valor_raw) VALUES (?, ?, ?)", pedidos_fonte)
    conn.commit()
    
    print("-> Registros 'pousados' na Staging Area:")
    staging_df = pd.read_sql_query("SELECT * FROM staging_pedidos", conn)
    print(staging_df.to_string(index=False))

def demonstrar_carga_completa_vs_incremental(conn: sqlite3.Connection):
    """
    2. CARGA COMPLETA vs INCREMENTAL:
    Demonstra a captura de registros novos usando coluna de controle 'data_atualizacao'.
    """
    print("\n" + "=" * 70)
    print("2. CONCEITO: CARGA COMPLETA vs CARGA INCREMENTAL")
    print("=" * 70)
    
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tabela_destino (
            id TEXT PRIMARY KEY,
            nome TEXT,
            valor REAL,
            data_atualizacao TEXT
        )
    """)
    
    # Carga Inicial (Completa)
    cur.execute("INSERT OR REPLACE INTO tabela_destino VALUES ('1', 'Notebook', 4500.00, '2026-09-01 10:00:00')")
    cur.execute("INSERT OR REPLACE INTO tabela_destino VALUES ('2', 'Teclado', 250.00, '2026-09-01 10:00:00')")
    conn.commit()
    
    print("-> Estado da Tabela Destino após Carga Inicial:")
    print(pd.read_sql_query("SELECT * FROM tabela_destino", conn).to_string(index=False))
    
    # Novos dados gerados na fonte
    novos_dados_fonte = [
        {"id": "2", "nome": "Teclado RGB", "valor": 280.00, "data_atualizacao": "2026-09-05 14:00:00"}, # Alteração
        {"id": "3", "nome": "Monitor 27", "valor": 1600.00, "data_atualizacao": "2026-09-05 15:30:00"}, # Novo registro
    ]
    
    ultima_data_sincronizada = "2026-09-01 10:00:00"
    print(f"\n-> Ponto de Corte Incremental (High Watermark): {ultima_data_sincronizada}")
    
    incrementais = [d for d in novos_dados_fonte if d["data_atualizacao"] > ultima_data_sincronizada]
    print(f"-> Apenas {len(incrementais)} registros elegíveis para carga incremental (evita reprocessar a tabela inteira!).")
    
    for item in incrementais:
        cur.execute("""
            INSERT INTO tabela_destino (id, nome, valor, data_atualizacao)
            VALUES (:id, :nome, :valor, :data_atualizacao)
            ON CONFLICT(id) DO UPDATE SET
                nome = excluded.nome,
                valor = excluded.valor,
                data_atualizacao = excluded.data_atualizacao
        """, item)
    conn.commit()
    
    print("\n-> Estado da Tabela Destino após Carga Incremental (UPSERT):")
    print(pd.read_sql_query("SELECT * FROM tabela_destino", conn).to_string(index=False))

def demonstrar_idempotencia():
    """
    3. IDEMPOTÊNCIA SOB PROVA:
    Compara um pipeline não-idempotente (que duplica dados a cada reexecução)
    com um pipeline idempotente (que mantém a integridade dos dados).
    """
    print("\n" + "=" * 70)
    print("3. CONCEITO: IDEMPOTÊNCIA (TOLERÂNCIA A REEXECUÇÕES)")
    print("=" * 70)
    
    # 3.1 Pipeline NÃO Idempotente (Problema de Duplicação)
    db_nao_idempotente = sqlite3.connect(":memory:")
    cur_nao_idemp = db_nao_idempotente.cursor()
    cur_nao_idemp.execute("CREATE TABLE log_vendas (venda_id TEXT, valor REAL)")
    
    def carga_com_duplicacao():
        cur_nao_idemp.execute("INSERT INTO log_vendas VALUES ('V1', 100.0)")
        cur_nao_idemp.execute("INSERT INTO log_vendas VALUES ('V2', 200.0)")
        db_nao_idempotente.commit()
    
    carga_com_duplicacao() # Execução 1
    carga_com_duplicacao() # Execução 2 (reexecução de retry)
    qtd_duplicada = cur_nao_idemp.execute("SELECT COUNT(*) FROM log_vendas").fetchone()[0]
    print(f"[FALHA DE IDEMPOTÊNCIA] Executado 2 vezes sem TRUNCATE/UPSERT:")
    print(f"   -> Esperado: 2 linhas | Atual no banco: {qtd_duplicada} linhas (DADOS DUPLICADOS!)")
    
    # 3.2 Pipeline IDEMPOTENTE (Técnica: TRUNCATE / DELETE + RELOAD ou UPSERT)
    db_idempotente = sqlite3.connect(":memory:")
    cur_idemp = db_idempotente.cursor()
    cur_idemp.execute("CREATE TABLE log_vendas (venda_id TEXT PRIMARY KEY, valor REAL)")
    
    def carga_idempotente():
        # Técnica TRUNCATE + INSERT (ou UPSERT)
        cur_idemp.execute("DELETE FROM log_vendas") # Equivalente a TRUNCATE
        cur_idemp.execute("INSERT INTO log_vendas VALUES ('V1', 100.0)")
        cur_idemp.execute("INSERT INTO log_vendas VALUES ('V2', 200.0)")
        db_idempotente.commit()
        
    carga_idempotente() # Execução 1
    carga_idempotente() # Execução 2
    carga_idempotente() # Execução 3
    qtd_idempotente = cur_idemp.execute("SELECT COUNT(*) FROM log_vendas").fetchone()[0]
    print(f"[SUCESSO DE IDEMPOTÊNCIA] Executado 3 vezes com padrão de Idempotência:")
    print(f"   -> Esperado: 2 linhas | Atual no banco: {qtd_idempotente} linhas (INTEGRIDADE PRESERVADA!)")

if __name__ == "__main__":
    banco = sqlite3.connect(":memory:")
    demonstrar_staging_area(banco)
    demonstrar_carga_completa_vs_incremental(banco)
    demonstrar_idempotencia()
    banco.close()
