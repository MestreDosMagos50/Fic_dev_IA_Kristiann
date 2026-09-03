import requests
import os
from urllib.parse import urlparse

def baixar_arquivo(url: str, destino: str, chunk_kb: int = 256) -> None:
    """Baixa um arquivo de qualquer tamanho usando streaming."""
    chunk_size = chunk_kb * 1024 # bytes
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    with requests.get(url, headers=headers, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        
        # Tamanho total do arquivo
        total = int(resp.headers.get('Content-Length', 0))
        if total:
            print(f'Tamanho: {total / (1024**2):.1f} MB')
            
        baixado = 0
        with open(destino, 'wb') as arq:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk: # filtra chunks vazios
                    arq.write(chunk)
                    baixado += len(chunk)
                    if total:
                        pct = baixado / total * 100
                        print(f'\r Progresso: {pct:.1f}%', end='')
                        
        print(f'\nArquivo salvo em: {destino}')
        print(f'Tamanho real: {baixado / 1024:.1f} KB')

if __name__ == '__main__':
    url_pdf = 'https://biblioteca.ibge.gov.br/visualizacao/livros/liv101957_informativo.pdf'
    baixar_arquivo(url_pdf, 'liv101957_informativo.pdf')
