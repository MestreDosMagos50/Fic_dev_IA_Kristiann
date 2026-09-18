"""
03_etl_bi_vs_elt_bigdata.py — Comparativo Detalhado: ETL (BI Tradicional) vs ELT (Big Data)
Módulo 2 / Aula 01 — FIC Engenharia de Dados

Objetivo:
Explicar conceitual e praticamente os dois grandes paradigmas da indústria da dados,
suas forças, fraquezas e a matriz de decisão arquitetural.
"""

import time
import pandas as pd

def exibir_matriz_comparativa():
    """Imprime a tabela comparativa oficial presente na apostila da aula."""
    matriz = [
        {
            "Aspecto": "Contexto de Origem",
            "ETL (BI Tradicional)": "Data warehouses, anos 1990 (Kimball, Inmon)",
            "ELT (Big Data)": "Data lakes e nuvem, anos 2010 (Hadoop, Snowflake, BigQuery)"
        },
        {
            "Aspecto": "Escopo de Processamento",
            "ETL (BI Tradicional)": "Todos os dados passam pelo pipeline antes da carga",
            "ELT (Big Data)": "Carga total; somente a fatia de interesse é transformada sob demanda"
        },
        {
            "Aspecto": "Momento da Estrutura",
            "ETL (BI Tradicional)": "Schema-on-write (estrutura imposta na gravação)",
            "ELT (Big Data)": "Schema-on-read (estrutura aplicada na consulta)"
        },
        {
            "Aspecto": "Volume Típico",
            "ETL (BI Tradicional)": "Gigabytes",
            "ELT (Big Data)": "Terabytes a Petabytes"
        },
        {
            "Aspecto": "Dado Bruto Preservado?",
            "ETL (BI Tradicional)": "Geralmente não (apenas os dados tratados)",
            "ELT (Big Data)": "Sim (repositório bruto e imutável)"
        },
        {
            "Aspecto": "Risco Característico",
            "ETL (BI Tradicional)": "Rigidez a mudanças e retrabalho se a regra mudar",
            "ELT (Big Data)": "\"Pântano de dados\" (Data Swamp) sem governança"
        },
    ]
    
    df_matriz = pd.DataFrame(matriz)
    print("=" * 90)
    print("           MATRIZ COMPARATIVA: ETL (BI TRADICIONAL) vs ELT (BIG DATA)")
    print("=" * 90)
    print(df_matriz.to_string(index=False))
    print("=" * 90)

def exibir_analogia_cozinha():
    """Exibe a analogia didática citada no material para fixação intuitiva."""
    print("\n" + "=" * 90)
    print("                      DICA DIDÁTICA: A ANALOGIA DA COZINHA")
    print("=" * 90)
    print("• ETL é o Restaurante Buffet Executivo:")
    print("  Prepara todo o cardápio e corta todos os legumes ANTES de abrir as portas.")
    print("  Tudo sai com apresentação padronizada e calibrada.")
    print("  Porém: o prato que não for consumido no dia vira desperdício de trabalho prévio.")
    print("\n• ELT é a Despensa Gigante de Ingredientes Crus:")
    print("  Armazena sacas inteiras de grãos, carnes e legumes frescos em grande escala.")
    print("  Cozinha-se estritamente o prato pedido pelo cliente, na hora exata do pedido.")
    print("  Vantagem: flexibilidade total para inventar novos pratos sem descartar a matéria-prima.")
    print("=" * 90)

def simulacao_de_custo_e_tempo():
    """Simula o comportamento e trade-offs computacionais de ambos os padrões."""
    print("\n### SIMULAÇÃO DE CENÁRIO: Ingestão de 100.000 Registros Heterogêneos ###\n")
    
    # Simulação ETL
    inicio_etl = time.time()
    print("[Pipeline ETL Tradicional]")
    print("1. Extraindo 100.000 linhas da fonte de CRM...")
    print("2. Servidor intermediário limpando e normalizando todas as 100.000 linhas (CPU intensiva)...")
    print("3. Carregando apenas as linhas válidas na tabela relacional 'dim_cliente'...")
    tempo_etl = 0.45  # simulação representativa
    print(f"-> Tempo total de ingestão ETL: {tempo_etl:.2f}s")
    print("-> Consulta Analítica (MT): instantânea (0.01s), pois os dados já estão mastigados.\n")
    
    # Simulação ELT
    inicio_elt = time.time()
    print("[Pipeline ELT Moderno]")
    print("1. Extraindo 100.000 linhas da fonte de CRM...")
    print("2. Despejando os dados brutos como JSON/Parquet diretamente no Data Lake...")
    tempo_elt_load = 0.08
    print(f"-> Carga inicial bruta: {tempo_elt_load:.2f}s (ultrarrápida!)")
    print("3. Usuário solicita: 'Vendas de MT'. Engine do banco executa SQL sobre os 5.000 registros relevantes...")
    tempo_elt_query = 0.05
    print(f"-> Tempo da transformação sob demanda: {tempo_elt_query:.2f}s")
    print(f"-> Tempo total (Carga + Consulta MT): {tempo_elt_load + tempo_elt_query:.2f}s")
    
    print("\nRESUMO PRÁTICO:")
    print("- Se seus dados são altamente estruturados e bem conhecidos: ETL garante integridade absoluta.")
    print("- Se seus dados são volumosos, variados ou as perguntas mudam constantemente: ELT oferece agilidade.")

if __name__ == "__main__":
    exibir_matriz_comparativa()
    exibir_analogia_cozinha()
    simulacao_de_custo_e_tempo()
