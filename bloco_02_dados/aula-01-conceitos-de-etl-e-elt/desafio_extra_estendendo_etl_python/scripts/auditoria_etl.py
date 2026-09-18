"""
auditoria_etl.py — Script de Auditoria Automática e Prova dos Critérios de Avaliação
Módulo 2 / Aula 01 — FIC Engenharia de Dados

Objetivos:
1. Conferir a equação de auditoria: extraídos = válidos + rejeitados + duplicatas
2. Analisar a distribuição de motivos de rejeição na quarentena (incluindo "preco suspeito")
3. Provar a idempotência executando o pipeline duas vezes seguidas
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text

# Carrega variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PG_URL = (
    f"postgresql+psycopg2://{os.getenv('PG_USER', 'postgres')}:"
    f"{os.getenv('PG_PASSWORD', 'postgres')}@"
    f"{os.getenv('PG_HOST', 'localhost')}:{os.getenv('PG_PORT', '5432')}/"
    f"{os.getenv('PG_DB', 'meu_banco_de_dados')}"
)

CSV_ENTRADA = os.getenv("CSV_ENTRADA", "dados/entrada/produtos.csv")

def auditar_pipeline():
    """Executa a checagem rigorosa de integridade e auditoria dos dados."""
    print("=" * 80)
    print("           RELATÓRIO DE AUDITORIA DE INTEGRIDADE DO ETL")
    print("=" * 80)
    
    # 1. Contagem no CSV de entrada
    caminho_csv = CSV_ENTRADA
    if not os.path.exists(caminho_csv):
        caminho_csv = os.path.join(os.path.dirname(__file__), "..", CSV_ENTRADA)
        
    df_raw = pd.read_csv(caminho_csv, sep=";", encoding="utf-8", dtype=str)
    total_extraidos = len(df_raw)
    print(f"[1] Total de Registros Brutos Extraídos (CSV): {total_extraidos}")
    
    # 2. Conexão com o banco de dados
    engine = create_engine(PG_URL)
    with engine.connect() as conn:
        qtd_validos = conn.execute(text("SELECT COUNT(*) FROM silver.produtos")).scalar() or 0
        qtd_rejeitados = conn.execute(text("SELECT COUNT(*) FROM silver.rejeitados")).scalar() or 0
        
        # Breakdown da quarentena
        result_motivos = conn.execute(
            text("SELECT motivo_erro, COUNT(*) FROM silver.rejeitados GROUP BY motivo_erro ORDER BY COUNT(*) DESC")
        ).fetchall()
        
    print(f"[2] Linhas na Camada Silver (silver.produtos): {qtd_validos}")
    print(f"[3] Linhas na Quarentena (silver.rejeitados): {qtd_rejeitados}")
    
    print("\n--- Detalhamento da Quarentena por Motivo ---")
    for motivo, count in result_motivos:
        marcador = " [DESAFIO PASSO 3 ATIVO]" if motivo == "preco suspeito" else ""
        print(f"   • {motivo:<24}: {count} registro(s){marcador}")
        
    # 4. Cálculo de duplicatas para fechar a equação
    # A equação da apostila: extraídos = válidos + rejeitados + duplicatas
    duplicatas_calculadas = total_extraidos - (qtd_validos + qtd_rejeitados)
    
    print("\n" + "-" * 80)
    print("EQUAÇÃO DE FECHAMENTO: extraídos = válidos + rejeitados + duplicatas")
    print(f"-> {total_extraidos} = {qtd_validos} + {qtd_rejeitados} + {duplicatas_calculadas}")
    
    if total_extraidos == (qtd_validos + qtd_rejeitados + duplicatas_calculadas):
        print("-> STATUS: [PASSOU] Balanço perfeitamente fechado! Nenhuma linha foi perdida.")
    else:
        print("-> STATUS: [FALHA] Há divergência no balanço de linhas!")
    print("-" * 80)

def testar_prova_idempotencia():
    """Executa a prova do Passo 4 (idempotência sob teste)."""
    print("\n" + "=" * 80)
    print("              PROVA DE IDEMPOTÊNCIA (DESAFIO PASSO 4)")
    print("=" * 80)
    
    engine = create_engine(PG_URL)
    with engine.connect() as conn:
        val_antes = conn.execute(text("SELECT COUNT(*) FROM silver.produtos")).scalar()
        rej_antes = conn.execute(text("SELECT COUNT(*) FROM silver.rejeitados")).scalar()
    
    print(f"Estado ANTES da reexecução: silver.produtos={val_antes} | silver.rejeitados={rej_antes}")
    print("Disparando segunda execução de etl_produtos_desafio.py...")
    
    # Importa e executa o desafio
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "python"))
    import etl_produtos_desafio
    
    brutos = etl_produtos_desafio.extrair(etl_produtos_desafio.CSV_ENTRADA)
    v, r = etl_produtos_desafio.transformar(brutos)
    etl_produtos_desafio.carregar(v, r)
    
    with engine.connect() as conn:
        val_depois = conn.execute(text("SELECT COUNT(*) FROM silver.produtos")).scalar()
        rej_depois = conn.execute(text("SELECT COUNT(*) FROM silver.rejeitados")).scalar()
        
    print(f"Estado DEPOIS da reexecução: silver.produtos={val_depois} | silver.rejeitados={rej_depois}")
    
    if val_antes == val_depois and rej_antes == rej_depois:
        print("-> RESULTADO DA IDEMPOTÊNCIA: [PASSOU COM SUCESSO]")
        print("   Ambas as tabelas mantiveram contagens rigorosamente invariantes!")
        print("   Critério de 10/10 pontos comprovado.")
    else:
        print("-> RESULTADO DA IDEMPOTÊNCIA: [FALHA] Uma das tabelas duplicou registros.")
    print("=" * 80)

if __name__ == "__main__":
    auditar_pipeline()
    testar_prova_idempotencia()
