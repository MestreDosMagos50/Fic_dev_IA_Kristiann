# ==============================================================================
# Aula 15: Embeddings e Busca Semântica
# Módulo 4: Persistindo e Carregando Embeddings
# ==============================================================================
"""
Salvar os embeddings em disco (com NumPy e JSON) elimina o custo computacional
em execuções seguintes, o que é essencial em ambientes de produção.
"""

import numpy as np
import json
from pathlib import Path

# ------------------------------------------------------------------------------
# 4.1 Salvar e Carregar com NumPy
# ------------------------------------------------------------------------------
def salvar_indice(embeddings: np.ndarray, metadados: list[dict], pasta: str | Path) -> None:
    """
    Salva embeddings (.npy) e metadados (.json) em disco.
    pasta/ deve existir ou será criada.
    """
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    
    # Salvar matriz de embeddings em formato binário NumPy
    np.save(pasta / 'embeddings.npy', embeddings)
    
    # Salvar metadados (texto, chunk_id, pagina, etc.) em JSON
    with open(pasta / 'metadados.json', 'w', encoding='utf-8') as f:
        json.dump(metadados, f, ensure_ascii=False, indent=2)
        
    print(f'Índice salvo: {embeddings.shape[0]} vetores em {pasta}/')


def carregar_indice(pasta: str | Path) -> tuple[np.ndarray, list[dict]]:
    """Carrega embeddings e metadados do disco."""
    pasta = Path(pasta)
    embeddings = np.load(pasta / 'embeddings.npy')
    
    with open(pasta / 'metadados.json', encoding='utf-8') as f:
        metadados = json.load(f)
        
    print(f'Índice carregado: {embeddings.shape[0]} vetores ({embeddings.shape[1]}d)')
    return embeddings, metadados

if __name__ == "__main__":
    print("=== Testando Persistência de Embeddings ===")
    
    # 1. Criando dados fictícios (10 vetores aleatórios de 384 dimensões)
    embeddings_falsos = np.random.randn(10, 384).astype('float32') 
    metadados_falsos = [{'id': i, 'texto': f'Frase de exemplo número {i}'} for i in range(10)]
    pasta_teste = 'indice_teste'
    
    # 2. Salvando os dados no disco
    print("-> Salvando no disco...")
    salvar_indice(embeddings_falsos, metadados_falsos, pasta_teste)
    
    # 3. Carregando os dados de volta
    print("\n-> Lendo do disco...")
    emb_carregado, meta_carregado = carregar_indice(pasta_teste)
    
    # 4. Verificando o que foi salvo
    print("\n-> Verificando resultado:")
    print(f"O item 3 lido do arquivo json foi: '{meta_carregado[3]['texto']}'")
