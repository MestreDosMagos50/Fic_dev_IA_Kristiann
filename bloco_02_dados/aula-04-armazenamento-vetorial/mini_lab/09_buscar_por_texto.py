import psycopg2
from sentence_transformers import SentenceTransformer
import warnings

warnings.filterwarnings("ignore")

# IMPORTANTE: Coloque aqui a senha que você definiu para o banco!
SENHA_DO_BANCO = "postgres"

print("Carregando modelo CLIP...")
model = SentenceTransformer('clip-ViT-B-32')

# Texto de busca digitado pelo usuário (agora interativo!)
termo_busca = input("\nDigite o que você quer buscar nas imagens (ex: 'um felino', 'veículo rápido' ou 'mar'): ")
print(f"Buscando no banco de dados por: '{termo_busca}'...")

# O modelo transforma o TEXTO em um vetor de 512 números para comparar com as imagens!
vetor_texto = model.encode(termo_busca).tolist()

try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password=SENHA_DO_BANCO, host="localhost")
    cur = conn.cursor()

    # Consulta SQL no pgvector usando Distância Cosseno (<=>)
    query = """
    SELECT titulo, url_ou_caminho, embedding <=> %s AS distancia
    FROM catalogo_imagens
    ORDER BY distancia ASC
    LIMIT 2;
    """
    cur.execute(query, (str(vetor_texto),))
    resultados = cur.fetchall()

    print("\n--- Resultados mais semelhantes encontrados pela IA ---")
    for titulo, url, distancia in resultados:
        print(f"📸 Foto: {titulo}")
        print(f"📐 Distância: {distancia:.4f} (quanto menor, mais parecido)")
        print(f"🔗 Link: {url}\n")

    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Erro ao buscar no banco: {e}")
