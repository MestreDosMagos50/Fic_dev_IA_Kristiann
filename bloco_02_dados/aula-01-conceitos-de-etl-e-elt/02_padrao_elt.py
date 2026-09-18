"""
02_padrao_elt.py — Demonstração Didática do Padrão ELT (Extract, Load, Transform)
Módulo 2 / Aula 01 — FIC Engenharia de Dados

Conceito Central:
O ELT inverte as duas últimas etapas:
1. Extract (Extrai da fonte)
2. Load (Carrega IMEDIATAMENTE e sem tratamento no destino: Data Lake ou DW Moderno)
3. Transform (Transforma DEPOIS, dentro do próprio destino, geralmente via SQL)

Vantagens:
- Aproveita a imensa capacidade de computação paralela distribuída do banco/lake.
- Schema-on-read: a estrutura ou filtragem é aplicada no momento da leitura/consulta.
- Preserva o dado bruto para sempre: se a regra de negócio mudar amanhã, o dado histórico está intacto.
"""

import sqlite3
import json
import pandas as pd

# ==============================================================================
# 1. EXTRACT (Extração)
# Extração rápida de eventos brutos (logs, transações, cliques de usuários).
# ==============================================================================
def extrair_eventos_brutos() -> list[dict]:
    """Simula a extração de eventos contínuos e heterogêneos."""
    print("\n" + "=" * 60)
    print("ETAPA 1: EXTRACT (Extração Rápida de Dados Brutos)")
    print("=" * 60)
    
    eventos = [
        {"evento_id": 1, "payload": json.dumps({"cliente": "Pedro", "uf": "MT", "valor_centavos": 15000, "timestamp": "2026-09-10T10:00:00"})},
        {"evento_id": 2, "payload": json.dumps({"cliente": "Mariana", "uf": "SP", "valor_centavos": 23000, "timestamp": "2026-09-10T10:05:00"})},
        {"evento_id": 3, "payload": json.dumps({"cliente": "Lucas", "uf": "MT", "valor_centavos": 4500, "timestamp": "2026-09-10T10:12:00"})},
        {"evento_id": 4, "payload": json.dumps({"cliente": "Carla", "uf": "RJ", "valor_centavos": 89000, "timestamp": "2026-09-10T10:15:00"})},
        {"evento_id": 5, "payload": json.dumps({"cliente": "João", "uf": "MT", "valor_centavos": 32000, "timestamp": "2026-09-10T10:20:00"})},
    ]
    print(f"-> [Extract] {len(eventos)} eventos brutos coletados.")
    return eventos

# ==============================================================================
# 2. LOAD (Carga Imediata no Destino / Bronze Lake)
# O dado bruto entra diretamente no destino sem transformação pesada prévia.
# ==============================================================================
def carregar_lake_bruto(eventos: list[dict], conn: sqlite3.Connection) -> None:
    """Carrega dados no banco de destino em sua forma crua (Camada Bronze)."""
    print("\n" + "=" * 60)
    print("ETAPA 2: LOAD (Carga Imediata e Direta no Destino — Lake/Raw)")
    print("=" * 60)
    
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_events (
            id INTEGER PRIMARY KEY,
            dados_json TEXT,
            ingestado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    for ev in eventos:
        cursor.execute("INSERT INTO raw_events (id, dados_json) VALUES (?, ?)", (ev["evento_id"], ev["payload"]))
    conn.commit()
    
    print("-> Dados brutos gravados com sucesso no repositório de destino:")
    cursor.execute("SELECT id, dados_json, ingestado_em FROM raw_events")
    for row in cursor.fetchall():
        print(f"   Row [{row[0]}]: {row[1]}")

# ==============================================================================
# 3. TRANSFORM (Transformação sob demanda via SQL no próprio Destino)
# Exemplo citado na apostila:
# "Precisa analisar as compras de clientes de MT no último trimestre?
#  Transforma-se apenas esse recorte — os demais bilhões de eventos ficam brutos."
# ==============================================================================
def transformar_sob_demanda_sql(conn: sqlite3.Connection) -> None:
    """Executa a transformação delegando o esforço computacional ao destino (SQL)."""
    print("\n" + "=" * 60)
    print("ETAPA 3: TRANSFORM (Transformação Delegada no Destino via SQL)")
    print("=" * 60)
    print("-> Pergunta de Negócio: 'Qual o volume e ticket médio de compras de clientes do estado de MT?'")
    print("-> Em vez de transformar todos os estados, aplicamos a transformação sob demanda apenas em MT:")
    
    # Query SQL transformando JSON em colunas tipadas e agregando os dados
    query_sql = """
        SELECT 
            json_extract(dados_json, '$.uf') AS uf,
            COUNT(*) AS total_compras,
            SUM(CAST(json_extract(dados_json, '$.valor_centavos') AS REAL) / 100.0) AS faturamento_total_reais,
            AVG(CAST(json_extract(dados_json, '$.valor_centavos') AS REAL) / 100.0) AS ticket_medio_reais
        FROM raw_events
        WHERE json_extract(dados_json, '$.uf') = 'MT'
        GROUP BY uf
    """
    
    df_resultado = pd.read_sql_query(query_sql, conn)
    print("\nResultado Analítico Processado Diretamente no Destino (ELT):")
    print(df_resultado.to_string(index=False))
    print("\n[Conclusão ELT]: Apenas a fatia de interesse foi transformada. O dado bruto permanece intacto para novas análises.")

if __name__ == "__main__":
    print("### EXECUTANDO DEMONSTRAÇÃO DO PADRÃO ELT ###")
    conexao_banco = sqlite3.connect(":memory:")
    
    eventos_coletados = extrair_eventos_brutos()
    carregar_lake_bruto(eventos_coletados, conexao_banco)
    transformar_sob_demanda_sql(conexao_banco)
    
    conexao_banco.close()
