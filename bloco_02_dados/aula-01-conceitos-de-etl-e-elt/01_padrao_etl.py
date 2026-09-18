"""
01_padrao_etl.py — Demonstração Didática do Padrão ETL (Extract, Transform, Load)
Módulo 2 / Aula 01 — FIC Engenharia de Dados

Conceito Central:
O ETL clássico é o padrão tradicional do Business Intelligence (anos 1990).
A característica definidora é que a TRANSFORMAÇÃO acontece ANTES da CARGA.
O Data Warehouse (destino final) só recebe dados já validados, limpos e modelados.
Padrão arquitetural: Schema-on-write (a estrutura é imposta no momento da gravação).
"""

import pandas as pd
from datetime import datetime

# ==============================================================================
# 1. EXTRACT (Extração)
# Conectar-se às fontes (bancos, arquivos, APIs) e extrair os dados brutos.
# Os dados são extraídos no seu formato cru ("bronze"), sem interpretação rígida.
# ==============================================================================
def extrair_dados_brutos() -> list[dict]:
    """Simula a extração de dados brutos de múltiplos sistemas operacionais."""
    print("\n" + "=" * 60)
    print("ETAPA 1: EXTRACT (Extração de Dados Brutos)")
    print("=" * 60)
    
    dados_fonte = [
        {"id_venda": "1001", "cliente": "  ana silva ", "valor": "R$ 1.250,50", "data": "10/09/2026", "status": "PAGO"},
        {"id_venda": "1002", "cliente": "CARLOS SOUZA", "valor": "R$ 300,00", "data": "11/09/2026", "status": "pago"},
        {"id_venda": "1003", "cliente": "marcos lima", "valor": "-R$ 50,00", "data": "12/09/2026", "status": "CANCELADO"},
        {"id_venda": "1004", "cliente": "  ", "valor": "R$ 450,00", "data": "data_errada", "status": "PAGO"},
        {"id_venda": "1001", "cliente": "Ana Silva", "valor": "R$ 1.250,50", "data": "10/09/2026", "status": "PAGO"}, # Duplicata
    ]
    
    print(f"-> [Extract] {len(dados_fonte)} registros brutos extraídos da fonte.")
    for item in dados_fonte:
        print(f"   Cru: {item}")
    return dados_fonte

# ==============================================================================
# 2. TRANSFORM (Transformação)
# Em um servidor ou engine intermediária, realizamos:
# - Limpeza e padronização (trim, lowercase, uppercase)
# - Tipagem e parsing (moeda -> float, texto -> date)
# - Validação de integridade e regras de negócio
# - Deduplicação
# - Quarentena de registros inválidos
# ==============================================================================
def transformar_dados(dados_brutos: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Transforma, limpa e separa registros válidos de registros em quarentena."""
    print("\n" + "=" * 60)
    print("ETAPA 2: TRANSFORM (Limpeza, Validação e Modelagem)")
    print("=" * 60)
    
    df = pd.DataFrame(dados_brutos)
    
    # 2.1 Limpeza de textos
    df["cliente"] = df["cliente"].str.strip().str.title()
    df["status"] = df["status"].str.strip().str.upper()
    
    # 2.2 Tratamento monetário brasileiro ("R$ 1.250,50" -> 1250.50)
    df["valor_numerico"] = (
        df["valor"]
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    df["valor_numerico"] = pd.to_numeric(df["valor_numerico"], errors="coerce")
    
    # 2.3 Tratamento de datas (dd/mm/aaaa)
    df["data_formatada"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")
    
    # 2.4 Validações e Quarentena
    df["motivo_rejeicao"] = None
    df.loc[df["cliente"] == "", "motivo_rejeicao"] = "cliente_vazio"
    df.loc[df["valor_numerico"].isna(), "motivo_rejeicao"] = "valor_invalido"
    df.loc[df["valor_numerico"] <= 0, "motivo_rejeicao"] = "valor_nao_positivo"
    df.loc[df["data_formatada"].isna(), "motivo_rejeicao"] = "data_invalida"
    
    rejeitados = df[df["motivo_rejeicao"].notna()].copy()
    validos = df[df["motivo_rejeicao"].isna()].copy()
    
    # 2.5 Deduplicação pelo identificador de venda
    total_antes_dedup = len(validos)
    validos = validos.drop_duplicates(subset=["id_venda"], keep="first")
    duplicatas_removidas = total_antes_dedup - len(validos)
    
    print(f"-> [Transform] Validação concluída:")
    print(f"   Válidos: {len(validos)}")
    print(f"   Rejeitados (Quarentena): {len(rejeitados)}")
    print(f"   Duplicatas descartadas: {duplicatas_removidas}")
    
    return validos, rejeitados

# ==============================================================================
# 3. LOAD (Carga)
# Gravar o resultado pronto no destino final (Data Warehouse / Camada Silver).
# O destino só recebe dados perfeitamente higienizados e padronizados.
# ==============================================================================
def carregar_warehouse(validos: pd.DataFrame, rejeitados: pd.DataFrame) -> None:
    """Simula a gravação nos destinos finais do Data Warehouse."""
    print("\n" + "=" * 60)
    print("ETAPA 3: LOAD (Carga no Destino Modelado / Schema-on-Write)")
    print("=" * 60)
    
    # Colunas finais curadas do modelo dimensional / relacional
    dw_vendas = validos[["id_venda", "cliente", "valor_numerico", "data_formatada", "status"]].copy()
    dw_vendas.rename(columns={"valor_numerico": "valor_total", "data_formatada": "data_venda"}, inplace=True)
    
    print("-> Tabela Final: 'dw.f_vendas' (Dados prontos para consumo analítico):")
    print(dw_vendas.to_string(index=False))
    
    print("\n-> Tabela de Quarentena: 'dw.rejeitados' (Auditoria de qualidade):")
    quarentena_view = rejeitados[["id_venda", "cliente", "valor", "data", "motivo_rejeicao"]]
    print(quarentena_view.to_string(index=False))
    
    print("\n[Conclusão ETL]: Todo dado inserido na tabela analítica já passou por validação estrita.")

if __name__ == "__main__":
    print("### EXECUTANDO DEMONSTRAÇÃO DO PADRÃO ETL ###")
    dados_extraidos = extrair_dados_brutos()
    dados_validos, dados_rejeitados = transformar_dados(dados_extraidos)
    carregar_warehouse(dados_validos, dados_rejeitados)
