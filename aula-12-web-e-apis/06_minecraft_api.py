import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (se você gerou uma chave no playground)
load_dotenv()

# Algumas rotas e limites da Minecraft API podem requerer uma chave (API Key)
# Você pode gerar uma facilmente acessando: https://www.minecraftitems.xyz/playground
API_KEY = os.getenv('MINECRAFT_API_KEY', '')

BASE_URL = 'https://api.minecraftitems.xyz/api'

# Configurando os headers básicos
headers = {
    'Content-Type': 'application/json'
}

# Se você possuir a chave, a API provavelmente a aceita via Authorization ou X-API-Key
if API_KEY:
    headers['Authorization'] = f"Bearer {API_KEY}"

# ─── 1. Requisição GET: Baixando a imagem de um item (PNG) ───────────────
item_name = "diamond_sword"
print(f"Buscando a imagem do item: {item_name}...")

try:
    # Este endpoint retorna os bytes da imagem diretamente
    response = requests.get(
        f"{BASE_URL}/item/{item_name}/size=4", 
        headers=headers, 
        timeout=15
    )
    response.raise_for_status()
    
    # Como é um arquivo binário (PNG), salvamos usando 'wb' (write binary)
    with open(f"{item_name}.png", "wb") as f:
        f.write(response.content)
    print(f"✅ Sucesso! Imagem salva como '{item_name}.png'")

except requests.exceptions.RequestException as e:
    print(f"❌ Erro ao buscar o item: {e}")


# ─── 2. Requisição POST: Gerando um GIF Rotativo ─────────────────────────
print("\nGerando GIF rotativo de uma netherite_pickaxe (Isso pode demorar um pouco)...")
try:
    # O endpoint de GIF exige um payload (body) em JSON configurando a animação
    payload = {
        "itemName": "netherite_pickaxe",
        "frames": 36,     # Quantidade de quadros da animação
        "scale": 2,       # Tamanho da imagem
        "glint": True     # Adiciona o brilho roxo de encantamento
    }
    
    response_gif = requests.post(
        f"{BASE_URL}/item/gif/direct", 
        headers=headers, 
        json=payload, 
        timeout=45 # O limite de tempo é maior porque gerar o GIF pesa no servidor
    )
    response_gif.raise_for_status()
    
    with open("netherite_pickaxe.gif", "wb") as f:
        f.write(response_gif.content)
    print("✅ Sucesso! GIF salvo como 'netherite_pickaxe.gif'")

except requests.exceptions.HTTPError as e:
    print(f"❌ Erro da API (HTTP {e.response.status_code}): {e.response.text}")
except requests.exceptions.RequestException as e:
    print(f"❌ Erro de conexão ao gerar o GIF: {e}")

print("\nConcluído! Verifique a pasta do projeto para ver as imagens geradas.")
