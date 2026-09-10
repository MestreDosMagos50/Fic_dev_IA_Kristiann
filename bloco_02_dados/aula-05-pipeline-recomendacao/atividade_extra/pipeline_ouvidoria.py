import csv
import json
import psycopg2
import random

# Configurações do Banco de Dados
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

def ingest_servicos_csv(csv_file_path):
    conn = get_db_connection()
    cur = conn.cursor()
    with open(csv_file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader) # Pula o cabeçalho
        for row in reader:
            id_servico, secretaria, servico, descricao, prazo_dias = row
            # Simula a geração de um embedding de 3 dimensões
            embedding = [round(random.uniform(-1, 1), 3) for _ in range(3)]
            cur.execute(
                "INSERT INTO servicos_master (id, secretaria, servico, descricao, prazo_dias, embedding) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET secretaria = EXCLUDED.secretaria, servico = EXCLUDED.servico, descricao = EXCLUDED.descricao, prazo_dias = EXCLUDED.prazo_dias, embedding = EXCLUDED.embedding",
                (id_servico, secretaria, servico, descricao, prazo_dias, str(embedding))
            )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Serviços de '{csv_file_path}' ingeridos e embeddings gerados.")

def ingest_manifestacoes_json(json_file_path):
    conn = get_db_connection()
    cur = conn.cursor()
    with open(json_file_path, 'r') as f:
        manifestacoes_data = json.load(f)
        for manifestacao in manifestacoes_data:
            cur.execute(
                "INSERT INTO ouvidoria_raw (dados) VALUES (%s)",
                (json.dumps(manifestacao),)
            )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Manifestações de '{json_file_path}' ingeridas.")

def classificar_prioridade(texto, severidade):
    termos_criticos = ["acidente", "risco", "desabamento", "urgente", "queda", "morte"]
    if any(termo in texto.lower() for termo in termos_criticos) or severidade >= 5:
        return "CRÍTICA"
    elif severidade >= 4:
        return "ALTA"
    return "NORMAL"

def process_manifestacoes():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Limpa a tabela para reprocessamento
    cur.execute("TRUNCATE TABLE ouvidoria_processada;")
    
    cur.execute("SELECT id, dados FROM ouvidoria_raw;")
    raw_manifestacoes = cur.fetchall()
    
    for raw_id, raw_manifestacao in raw_manifestacoes:
        protocolo = raw_manifestacao.get("protocolo")
        bairro = raw_manifestacao.get("bairro")
        texto_relato = raw_manifestacao.get("texto_relato")
        severidade_declarada = raw_manifestacao.get("severidade_declarada")
        
        nivel_prioridade = classificar_prioridade(texto_relato, severidade_declarada)
        
        # Simula o embedding do texto_relato
        relato_embedding = [round(random.uniform(-1, 1), 3) for _ in range(3)]
        
        # Roteamento semântico
        cur.execute(
            """
            SELECT 
             s.id,
             s.embedding <=> %s AS distancia
            FROM servicos_master s
            ORDER BY distancia ASC
            LIMIT 1;
            """,
            (str(relato_embedding),)
        )
        servico_recomendado = cur.fetchone()
        servico_sugerido_id = servico_recomendado[0] if servico_recomendado else None
        distancia_confianca = servico_recomendado[1] if servico_recomendado else None
        
        cur.execute(
            "INSERT INTO ouvidoria_processada (protocolo, bairro, relato, nivel_prioridade, servico_sugerido_id, distancia_confianca) VALUES (%s, %s, %s, %s, %s, %s)",
            (protocolo, bairro, texto_relato, nivel_prioridade, servico_sugerido_id, distancia_confianca)
        )
    conn.commit()
    cur.close()
    conn.close()
    print("Manifestações processadas, prioridade classificada e roteamento realizado.")

if __name__ == "__main__":
    print("Iniciando pipeline de ouvidoria...")
    ingest_servicos_csv('servicos_municipais.csv')
    ingest_manifestacoes_json('manifestacoes_cidadao.json')
    process_manifestacoes()
    print("Pipeline da ouvidoria concluído.")
