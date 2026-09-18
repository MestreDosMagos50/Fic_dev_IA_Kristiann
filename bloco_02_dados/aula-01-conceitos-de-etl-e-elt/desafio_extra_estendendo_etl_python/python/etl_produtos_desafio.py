"""
etl_produtos_desafio.py — ETL Completo com Solução dos Desafios (Passos 3 e 4)
Módulo 2 / Aula 01 — FIC Engenharia de Dados

Implementações dos Desafios da Apostila:
1. Passo 3: Nova regra de negócio — produtos com preço acima de R$ 50.000,00
   vão para a quarentena com o motivo "preco suspeito".
2. Passo 4: Correção de Idempotência — garantia de que a tabela silver.rejeitados
   não duplique registros ao ser executada consecutivas vezes.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text

# Carrega variáveis de ambiente de .env se a biblioteca python-dotenv estiver instalada
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------- Configuração (nunca deixe senha no código!) ----------
PG_URL = (
    f"postgresql+psycopg2://{os.getenv('PG_USER', 'postgres')}:"
    f"{os.getenv('PG_PASSWORD', 'postgres')}@"
    f"{os.getenv('PG_HOST', 'localhost')}:{os.getenv('PG_PORT', '5432')}/"
    f"{os.getenv('PG_DB', 'meu_banco_de_dados')}"
)

CSV_ENTRADA = os.getenv("CSV_ENTRADA", "dados/entrada/produtos.csv")
CATEGORIAS_VALIDAS = {"eletronicos", "livros", "casa", "esporte", "moda"}
VALOR_LIMITE_SUSPEITO = 50000.00

# ---------- E: Extract ----------
def extrair(caminho_csv: str) -> pd.DataFrame:
    """Lê o CSV bruto. Tudo como string: o bronze não interpreta nada."""
    if not os.path.exists(caminho_csv):
        caminho_alternativo = os.path.join(os.path.dirname(__file__), "..", caminho_csv)
        if os.path.exists(caminho_alternativo):
            caminho_csv = os.path.abspath(caminho_alternativo)

    df = pd.read_csv(caminho_csv, sep=";", encoding="utf-8", dtype=str)
    print(f"[E] {len(df)} linhas extraídas de {caminho_csv}")
    return df

# ---------- T: Transform ----------
def transformar(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Limpa, valida e separa válidos de rejeitados (quarentena)."""
    df = df.copy()

    # Limpeza de texto: trim + capitalização do nome
    df["nome"] = df["nome"].str.strip().str.title()
    df["categoria"] = df["categoria"].str.strip().str.lower()

    # Preço: "R$ 1.234,56" -> 1234.56
    df["preco"] = (
        df["preco"]
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)  # remove separador de milhar
        .str.replace(",", ".", regex=False)  # vírgula decimal -> ponto
        .str.strip()
    )
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce")

    # Data: "dd/mm/aaaa" -> date (inconvertíveis viram NaT)
    df["data_cadastro"] = pd.to_datetime(
        df["data_cadastro"], format="%d/%m/%Y", errors="coerce"
    )

    # ----- Validação: cada regra escreve o motivo da rejeição -----
    df["motivo_erro"] = None
    df.loc[df["nome"].isna() | (df["nome"] == ""), "motivo_erro"] = "nome vazio"
    df.loc[df["preco"].isna(), "motivo_erro"] = "preco invalido"
    df.loc[df["preco"] <= 0, "motivo_erro"] = "preco nao positivo"
    
    # --------------------------------------------------------------------------
    # PASSO 3 — DESAFIO: NOVA REGRA DE VALIDAÇÃO ("preco suspeito")
    # Produtos com valor acima de R$ 50.000,00 vão para quarentena.
    # --------------------------------------------------------------------------
    df.loc[df["preco"] > VALOR_LIMITE_SUSPEITO, "motivo_erro"] = "preco suspeito"
    
    df.loc[df["data_cadastro"].isna(), "motivo_erro"] = "data invalida"
    df.loc[~df["categoria"].isin(CATEGORIAS_VALIDAS), "motivo_erro"] = (
        "categoria desconhecida"
    )

    rejeitados = df[df["motivo_erro"].notna()].copy()
    validos = df[df["motivo_erro"].isna()].drop(columns=["motivo_erro"])

    # Deduplicação pelo código do produto (mantém a primeira ocorrência)
    antes = len(validos)
    validos = validos.drop_duplicates(subset=["codigo"], keep="first")
    print(
        f"[T] {len(validos)} válidos | {len(rejeitados)} rejeitados | "
        f"{antes - len(validos)} duplicatas removidas"
    )
    return validos, rejeitados

# ---------- L: Load ----------
def carregar(validos: pd.DataFrame, rejeitados: pd.DataFrame) -> None:
    """
    Grava no PostgreSQL com IDEMPOTÊNCIA COMPLETA (Válidos e Quarentena).
    
    DIAGNÓSTICO DO PASSO 4:
    No script baseline, a tabela silver.produtos recebia TRUNCATE antes do append,
    garantindo idempotência. Já a silver.rejeitados recebia apenas 'append' sem limpeza,
    fazendo com que cada execução acumulasse cópias duplicadas dos rejeitados.
    
    CORREÇÃO DO PASSO 4:
    Executamos uma limpeza prévia (TRUNCATE ou DELETE por pipeline_origem) em
    silver.rejeitados antes da inserção, tornando o pipeline 100% idempotente.
    """
    engine = create_engine(PG_URL)
    pipeline_id = "etl_produtos_python"
    
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver"))
        
        # 1. Tabela silver.produtos
        conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS silver.produtos ("
                " codigo TEXT PRIMARY KEY, nome TEXT, categoria TEXT,"
                " preco NUMERIC(12,2), data_cadastro DATE)"
            )
        )
        
        # 2. Tabela silver.rejeitados estruturada
        conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS silver.rejeitados ("
                " codigo TEXT, nome TEXT, preco NUMERIC(12,2), categoria TEXT,"
                " data_cadastro DATE, motivo_erro TEXT, pipeline_origem TEXT)"
            )
        )
        
        # 3. Limpeza Idempotente: TRUNCATE em produtos e limpeza seletiva em rejeitados
        conn.execute(text("TRUNCATE TABLE silver.produtos"))
        conn.execute(
            text("DELETE FROM silver.rejeitados WHERE pipeline_origem = :origem"),
            {"origem": pipeline_id}
        )

    # Inserção dos registros no banco
    validos.to_sql(
        "produtos", engine, schema="silver", if_exists="append", index=False
    )
    
    rejeitados.assign(pipeline_origem=pipeline_id).to_sql(
        "rejeitados", engine, schema="silver", if_exists="append", index=False
    )
    
    print(
        f"[L - IDEMPOTENTE] {len(validos)} linhas em silver.produtos; "
        f"{len(rejeitados)} em silver.rejeitados (sem duplicação)"
    )

if __name__ == "__main__":
    print("=== EXECUTANDO ETL COM DESAFIOS (PASSOS 3 E 4) ===")
    brutos = extrair(CSV_ENTRADA)
    validos, rejeitados = transformar(brutos)
    carregar(validos, rejeitados)
    print("ETL com desafios concluído com sucesso.")
