import urllib.request
from PIL import Image
import psycopg2
from sentence_transformers import SentenceTransformer
import warnings
import os

warnings.filterwarnings("ignore")

# IMPORTANTE: Coloque aqui a senha que você definiu para o banco!
SENHA_DO_BANCO = "postgres"

print("Carregando modelo CLIP...")
model = SentenceTransformer('clip-ViT-B-32')

print("\n--- Busca Reversa de Imagens (Image-to-Image) ---")
# Para o teste, vamos usar a URL de uma foto de um cachorro pug
url_busca = "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=400"
print(f"Baixando imagem de busca: {url_busca}")

try:
    urllib.request.urlretrieve(url_busca, "busca_img.jpg")
    img_busca = Image.open("busca_img.jpg")

    # Passa a NOVA imagem para o CLIP e a transforma em vetor
    print("Processando imagem...")
    vetor_imagem = model.encode(img_busca).tolist()

    conn = psycopg2.connect(dbname="postgres", user="postgres", password=SENHA_DO_BANCO, host="localhost")
    cur = conn.cursor()

    # Consulta no SQL os vizinhos mais próximos dessa imagem
    query = """
    SELECT titulo, url_ou_caminho, embedding <=> %s AS distancia
    FROM catalogo_imagens
    ORDER BY distancia ASC
    LIMIT 2;
    """
    cur.execute(query, (str(vetor_imagem),))
    resultados = cur.fetchall()

    print("\n--- As fotos do catálogo mais parecidas com essa imagem são: ---")
    for titulo, url, distancia in resultados:
        print(f"📸 Foto: {titulo}")
        print(f"📐 Distância: {distancia:.4f}")
        print(f"🔗 Link: {url}\n")

    cur.close()
    conn.close()
    
    if os.path.exists("busca_img.jpg"):
        os.remove("busca_img.jpg")
        
except Exception as e:
    print(f"❌ Erro na busca: {e}")
