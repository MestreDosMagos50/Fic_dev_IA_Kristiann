import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Usar 'with' garante que a sessão feche sozinha
with requests.Session() as session:
    session.headers.update({
        'Accept': 'application/json',
        'User-Agent': 'MeuScript/1.0',
        # 'X-API-Key': os.getenv('MINHA_API_KEY', 'chave_temporaria')
    })
    
    print("--- Usando a Session em um Loop ---")
    for pagina in range(1, 4):
        resp = session.get(
            'https://jsonplaceholder.typicode.com/posts',
            params={'_page': pagina, '_limit': 5},
            timeout=10
        )
        resp.raise_for_status()
        dados = resp.json()
        print(f'Página {pagina}: {len(dados)} itens recebidos com sucesso!')
