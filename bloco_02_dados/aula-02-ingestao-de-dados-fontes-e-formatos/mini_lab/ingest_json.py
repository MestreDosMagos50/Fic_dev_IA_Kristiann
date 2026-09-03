import json
import psycopg2

DB_HOST = "localhost"
DB_NAME = "TESTE"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

def ingest_json_to_postgres(json_file_path, table_name):
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        
        # Criar tabela com campos específicos e JSONB para os itens
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            pedido_id VARCHAR(50),
            cliente_id VARCHAR(50),
            data DATE,
            itens JSONB
        );
        """)
        conn.commit()
        
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            for record in data:
                pedido_id = record.get('pedido_id')
                cliente_id = record.get('cliente_id')
                data_pedido = record.get('data')
                # Mantém os itens como JSON
                itens_json = json.dumps(record.get('itens', []))
                
                cur.execute(f"INSERT INTO {table_name} (pedido_id, cliente_id, data, itens) VALUES (%s, %s, %s, %s)", 
                            (pedido_id, cliente_id, data_pedido, itens_json))
            conn.commit()
            print(f"Dados do JSON '{json_file_path}' ingeridos com sucesso na tabela '{table_name}'.")
    except Exception as e:
        print(f"Erro ao ingerir dados JSON: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    ingest_json_to_postgres('pedidos.json', 'pedidos_estruturados')
