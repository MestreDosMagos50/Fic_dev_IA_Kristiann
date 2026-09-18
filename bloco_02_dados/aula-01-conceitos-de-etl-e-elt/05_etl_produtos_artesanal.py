"""
05_etl_produtos_artesanal.py — ETL Completo em Python Puro (Código da Seção 5 da Apostila)
Módulo 2 / Aula 01 — FIC Engenharia de Dados

Extract:   dados/entrada/produtos.csv
Transform: Limpeza de preço, data, texto; validação; deduplicação
Load:      silver.produtos (válidos) e silver.rejeitados (quarentena)
"""

import os
import io
import pandas as pd
from sqlalchemy import create_engine, text

# ---------- Configuração (nunca deixe senha no código!) ----------
PG_URL = (
    f"postgresql+psycopg2://{os.getenv('PG_USER', 'postgres')}:"
    f"{os.getenv('PG_PASSWORD', 'postgres')}@"
    f"{os.getenv('PG_HOST', 'localhost')}:{os.getenv('PG_PORT', '5432')}/"
    f"{os.getenv('PG_DB', 'meu_banco_de_dados')}"
)

# Caminho do arquivo de entrada conforme especificado na apostila
CSV_ENTRADA = os.getenv("CSV_ENTRADA", "desafio_extra_estendendo_etl_python/dados/entrada/produtos.csv")
CATEGORIAS_VALIDAS = {"eletronicos", "livros", "casa", "esporte", "moda"}

# ---------- E: Extract ----------
def extrair(caminho_csv: str) -> pd.DataFrame:
    """Lê o CSV bruto. Tudo como string: o bronze não interpreta nada."""
    if not os.path.exists(caminho_csv):
        print(f"[AVISO] Arquivo '{caminho_csv}' não encontrado no caminho relativo. Utilizando dados de demonstração em memória...")
        csv_exemplo = (
            "codigo;nome;preco;categoria;data_cadastro\n"
            "P001;  notebook dell ;R$ 4.500,00;eletronicos;15/01/2026\n"
            "P002;mouse logitech;R$ 150,00;eletronicos;20/01/2026\n"
            "P003;;R$ 80,00;livros;22/01/2026\n"
            "P004;cadeira gamer;R$ -100,00;casa;25/01/2026\n"
            "P005;cafeteira expresso;R$ 350,00;eletrodomesticos;28/01/2026\n"
            "P006;tenis corrida;R$ 400,00;esporte;data_invalida\n"
            "P001;Notebook Dell;R$ 4.500,00;eletronicos;15/01/2026\n"
        )
        df = pd.read_csv(io.StringIO(csv_exemplo), sep=";", encoding="utf-8", dtype=str)
    else:
        df = pd.read_csv(caminho_csv, sep=";", encoding="utf-8", dtype=str)
        
    print(f"[E] {len(df)} linhas extraídas.")
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
    df.loc[df["data_cadastro"].isna(), "motivo_erro"] = "data invalida"
    df.loc[~df["categoria"].isin(CATEGORIAS_VALIDAS), "motivo_erro"] = "categoria desconhecida"

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
    """Grava no PostgreSQL. TRUNCATE + append = carga idempotente."""
    try:
        engine = create_engine(PG_URL)
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver"))
            conn.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS silver.produtos ("
                    " codigo TEXT PRIMARY KEY, nome TEXT, categoria TEXT,"
                    " preco NUMERIC(12,2), data_cadastro DATE)"
                )
            )
            conn.execute(text("TRUNCATE TABLE silver.produtos"))

        validos.to_sql(
            "produtos", engine, schema="silver", if_exists="append", index=False
        )
        rejeitados.assign(pipeline_origem="etl_produtos_python").to_sql(
            "rejeitados", engine, schema="silver", if_exists="append", index=False
        )
        print(
            f"[L] {len(validos)} linhas em silver.produtos; "
            f"{len(rejeitados)} em silver.rejeitados"
        )
    except Exception as err:
        print(f"[L - FALHA BANCO] Não foi possível conectar ao PostgreSQL: {err}")
        print("[L - SIMULAÇÃO] Exibindo tabelas que seriam gravadas:")
        print("\n--- silver.produtos (Válidos) ---")
        print(validos.to_string(index=False))
        print("\n--- silver.rejeitados (Quarentena) ---")
        print(rejeitados.to_string(index=False))

if __name__ == "__main__":
    print("=== EXECUTANDO PIPELINE ETL DE PRODUTOS (SEÇÃO 5) ===")
    brutos = extrair(CSV_ENTRADA)
    validos, rejeitados = transformar(brutos)
    carregar(validos, rejeitados)
    print("ETL concluído com sucesso.")
