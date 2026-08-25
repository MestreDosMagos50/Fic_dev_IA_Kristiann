# ==============================================================================
# Aula 15: Embeddings e Busca Semântica
# Módulo 1: O Que São Embeddings
# ==============================================================================
"""
Um embedding é uma função que mapeia texto em um vetor de números reais 
(tipicamente entre 384 e 1536 dimensões) preservando relações semânticas:
textos com significado similar são mapeados para vetores próximos no espaço.

A ideia de representar palavras como vetores existe desde o word2vec (2013),
mas modelos modernos (como BERT e sentence-transformers) geram embeddings
contextuais para uma frase inteira.
"""

from sentence_transformers import SentenceTransformer

# ------------------------------------------------------------------------------
# 1.2 Estrutura de um Vetor de Embedding
# ------------------------------------------------------------------------------
def explorar_vetor():
    modelo = SentenceTransformer('all-MiniLM-L6-v2') # 384 dimensoes
    texto = 'Contratos de prestação de serviço têm prazo determinado.'
    vetor = modelo.encode(texto)

    print(type(vetor)) # <class 'numpy.ndarray'>
    print(vetor.shape) # (384,)
    print(vetor.dtype) # float32
    print(vetor[:5])   # Primeiros valores
    
    # O modelo all-MiniLM-L6-v2 gera vetores já normalizados (norma = 1)
    print(f'Norma: {(vetor**2).sum()**0.5:.4f}') # ~ 1.0 (normalizado)

if __name__ == "__main__":
    explorar_vetor()
