"""
Módulo de Conexão com o Banco de Dados PostgreSQL
Suporta tanto conexão direta via psycopg2/SQLAlchemy quanto via Docker.
"""

import os
import subprocess
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Carregar variáveis de ambiente do .env se existir
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "superset_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "superset_password")
DB_NAME = os.getenv("DB_NAME", "superset_data")

def get_connection():
    """Tenta conectar ao PostgreSQL usando as credenciais configuradas."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
            connect_timeout=3
        )
        return conn
    except Exception as e_main:
        # Fallback para dados_user / dados caso esteja rodando diretamente com o container data_postgres
        try:
            conn = psycopg2.connect(
                host="localhost",
                port="5432",
                user="dados_user",
                password="dados_pass",
                dbname="superset_data",
                connect_timeout=3
            )
            return conn
        except Exception:
            raise e_main

def init_tables():
    """Cria a tabela nuvem_palavras_tech caso não exista."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS nuvem_palavras_tech (
        id SERIAL PRIMARY KEY,
        palavra VARCHAR(100) NOT NULL,
        categoria VARCHAR(50) NOT NULL,
        frequencia INT NOT NULL DEFAULT 1,
        data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_nuvem_palavra_data ON nuvem_palavras_tech (data_atualizacao DESC);
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_sql)
            conn.commit()
            print("✅ Tabela 'nuvem_palavras_tech' verificada/criada no PostgreSQL via conexão direta.")
            return True
    except Exception as e:
        # Se falhar conexão local direta por falta de porta mapeada, tenta via docker exec
        print(f"⚠️ Conexão direta falhou ({e}). Tentando provisionar via docker exec...")
        for container in ["data_postgres", "meu_postgres"]:
            cmd = ["docker", "exec", "-i", container, "psql", "-U", "superset_user", "-d", "superset_data", "-c", create_table_sql]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode == 0:
                print(f"✅ Tabela 'nuvem_palavras_tech' criada com sucesso via contêiner {container}!")
                return True
        print(f"❌ Não foi possível criar tabela automaticamente: {e}")
        return False

def salvar_palavras(lista_palavras):
    """Insere uma lista de dicionários [{'palavra': str, 'categoria': str, 'frequencia': int}] na tabela."""
    insert_sql = """
    INSERT INTO nuvem_palavras_tech (palavra, categoria, frequencia, data_atualizacao)
    VALUES (%s, %s, %s, CURRENT_TIMESTAMP);
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for item in lista_palavras:
                    cur.execute(insert_sql, (item["palavra"], item["categoria"], item["frequencia"]))
            conn.commit()
        return True
    except Exception as e:
        # Fallback via Docker exec se necessário
        targets = [
            ("superset_meta_db", "superset", "superset"),
            ("data_postgres", "superset_user", "superset_data"),
            ("data_postgres", "dados_user", "dados")
        ]
        values = []
        for item in lista_palavras:
            p = item["palavra"].replace("'", "''")
            c = item["categoria"].replace("'", "''")
            f = int(item["frequencia"])
            values.append(f"('{p}', '{c}', {f}, CURRENT_TIMESTAMP)")
        sql_batch = f"INSERT INTO nuvem_palavras_tech (palavra, categoria, frequencia, data_atualizacao) VALUES {', '.join(values)};"
        
        salvou = False
        for container, user, dbname in targets:
            try:
                cmd = ["docker", "exec", "-i", container, "psql", "-U", user, "-d", dbname, "-c", sql_batch]
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                if proc.returncode == 0:
                    salvou = True
            except Exception:
                pass
        if salvou:
            return True
        print(f"❌ Erro ao salvar palavras: {e}")
        return False

def consultar_top_palavras(limite=50):
    """Retorna as palavras mais recentes agrupadas por peso."""
    query = f"""
    SELECT
        palavra,
        categoria,
        SUM(frequencia) AS frequencia_total,
        MAX(data_atualizacao) AS ultima_atualizacao
    FROM nuvem_palavras_tech
    WHERE data_atualizacao >= CURRENT_TIMESTAMP - INTERVAL '30 minutes'
    GROUP BY palavra, categoria
    ORDER BY frequencia_total DESC
    LIMIT {limite};
    """
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                return cur.fetchall()
    except Exception as e:
        # Fallback via Docker
        cmd = ["docker", "exec", "-i", "data_postgres", "psql", "-U", "superset_user", "-d", "superset_data", "-c", query]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            print(proc.stdout)
        return []
