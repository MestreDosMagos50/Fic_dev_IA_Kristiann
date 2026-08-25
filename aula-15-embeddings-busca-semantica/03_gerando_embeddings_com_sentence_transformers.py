# ==============================================================================
# Aula 15: Embeddings e Busca Semântica
# Módulo 3: Gerando Embeddings com sentence-transformers
# ==============================================================================
"""
A biblioteca sentence-transformers é o padrão de mercado para geração de 
embeddings de texto em Python. Ela encapsula modelos BERT e similares.
"""

from sentence_transformers import SentenceTransformer
import numpy as np

# ------------------------------------------------------------------------------
# 3.2 Gerando Embeddings — API Básica
# ------------------------------------------------------------------------------
def exemplos_basicos():
    modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # Uma frase
    vec = modelo.encode('O contrato foi rescindido.')
    print("Vetor de uma frase:", vec.shape) # (384,)

    # Múltiplas frases de uma vez (batch) — muito mais eficiente
    textos = [
        'O contrato foi encerrado por ambas as partes.',
        'O acordo foi rescindido mutuamente.',
        'A taxa de juros subiu 0,25 pontos.',
        'O pagamento deve ser realizado até o dia 10.',
    ]
    
    embeddings = modelo.encode(
        textos,
        batch_size=32,            # processar N textos por vez
        normalize_embeddings=True,# garantir norma = 1 (recomendado)
        show_progress_bar=True,   # barra de progresso para lotes grandes
        convert_to_numpy=True     # retornar ndarray
    )
    print("Embeddings batch:", embeddings.shape)

# ------------------------------------------------------------------------------
# 3.3 Prefixo de Instrução para Modelos E5
# ------------------------------------------------------------------------------
def exemplo_modelo_e5():
    """Modelos intfloat/multilingual-e5-* exigem prefixo 'query:' ou 'passage:'."""
    modelo = SentenceTransformer('intfloat/multilingual-e5-small')
    
    documentos = [
        'passage: O contrato prevê multa de 20% em caso de rescisão antecipada.',
        'passage: O pagamento mensal é de R$ 5.000,00, vencendo todo dia 5.',
        'passage: A vigência do contrato é de 24 meses a partir da assinatura.',
    ]
    
    query = 'query: Qual é a penalidade por cancelar o contrato antes do prazo?'
    
    emb_docs = modelo.encode(documentos, normalize_embeddings=True)
    emb_query = modelo.encode(query, normalize_embeddings=True)
    
    scores = emb_docs @ emb_query
    for i, (doc, score) in enumerate(zip(documentos, scores)):
        print(f'{score:.4f} | {doc[9:60]}...')

if __name__ == "__main__":
    print("=== Rodando Exemplos Básicos ===")
    exemplos_basicos()
    print("\n=== Rodando Exemplo com Modelo E5 ===")
    exemplo_modelo_e5()
