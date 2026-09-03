"""
Aula 16 — Peça 1: Embeddings e Similaridade Cosseno
====================================================
Execute: python 02_embeddings.py

O que você verá:
  - Como gerar um embedding de uma sentença
  - Como processar múltiplas sentenças em batch
  - Como calcular a similaridade cosseno manualmente
  - Como interpretar os valores de similaridade

Dependências: pip install sentence-transformers numpy
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# ── 1. Similaridade cosseno manual ───────────────────────────────────────
def similaridade_cosseno(v1: np.ndarray, v2: np.ndarray) -> float:
    """Calcula a similaridade cosseno entre dois vetores.
    Resultado entre -1 e 1. Quanto mais próximo de 1, mais similares.
    """
    produto = np.dot(v1, v2)
    norma1  = np.linalg.norm(v1)
    norma2  = np.linalg.norm(v2)
    if norma1 == 0 or norma2 == 0:
        return 0.0
    return float(produto / (norma1 * norma2))

# Demonstração com vetores simples (dimensão 4)
print('=== Similaridade Cosseno Manual ===')
emb_contrato  = np.array([0.82, 0.15, 0.91, 0.33])
emb_acordo    = np.array([0.79, 0.18, 0.88, 0.31])
emb_culinaria = np.array([0.12, 0.95, 0.08, 0.77])

print(f'contrato vs acordo:    {similaridade_cosseno(emb_contrato, emb_acordo):.4f}')   # ~0.99
print(f'contrato vs culinaria: {similaridade_cosseno(emb_contrato, emb_culinaria):.4f}') # ~0.20

# ── 2. Embeddings reais com sentence-transformers ────────────────────────
print('\n=== Embeddings Reais — paraphrase-multilingual-MiniLM-L12-v2 ===')
modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Embedding de uma única sentença
sentenca  = 'O contrato de locação foi assinado em março de 2024.'
embedding = modelo.encode(sentenca)
print(f'Shape:       {embedding.shape}')    # (384,)
print(f'Dtype:       {embedding.dtype}')    # float32
print(f'Primeiros 5: {embedding[:5].round(4)}')

# ── 3. Batch encoding ────────────────────────────────────────────────────
print('\n=== Batch Encoding ===')
textos = [
    'O contrato foi assinado entre as partes.',
    'O acordo foi firmado pelos envolvidos.',       # sinônimo — deve ser próximo
    'Receita de bolo de cenoura com cobertura.',    # sem relação — deve ser distante
    'O valor do aluguel é de dois mil reais.',      # mesmo domínio — deve ser próximo
]

embeddings = modelo.encode(
    textos,
    batch_size=32,
    normalize_embeddings=True,   # norma = 1: obrigatório para cosseno
    show_progress_bar=True
)
print(f'Shape do batch: {embeddings.shape}')  # (4, 384)

# ── 4. Comparação entre todos ────────────────────────────────────────────
print('\n=== Similaridade entre as sentenças ===')
rotulos = ['contrato', 'acordo (sinônimo)', 'culinaria', 'aluguel']
for i in range(len(textos)):
    for j in range(i+1, len(textos)):
        sim = similaridade_cosseno(embeddings[i], embeddings[j])
        print(f'{rotulos[i]:<22} vs {rotulos[j]:<22}:  {sim:.4f}')

# ── 5. Interpretação ─────────────────────────────────────────────────────
print('\n=== Interpretação dos scores ===')
print('~1.0  = vetores idênticos (mesmo texto)')
print('>0.8  = muito similares (mesmo assunto)')
print('>0.5  = relacionados (mesmo domínio)')
print('<0.3  = sem relação semântica aparente')
