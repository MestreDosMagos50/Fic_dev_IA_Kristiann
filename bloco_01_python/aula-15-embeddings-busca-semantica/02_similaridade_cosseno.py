# ==============================================================================
# Aula 15: Embeddings e Busca Semântica
# Módulo 2: Similaridade Cosseno
# ==============================================================================
"""
A similaridade cosseno mede o ângulo entre dois vetores no espaço de alta dimensão.
Ela ignora a magnitude dos vetores e foca apenas em sua direção (conteúdo semântico).
"""

import numpy as np

# ------------------------------------------------------------------------------
# 2.2 Implementação Manual e com NumPy
# ------------------------------------------------------------------------------
def similaridade_cosseno(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Calcula a similaridade cosseno entre dois vetores."""
    norma_a = np.linalg.norm(vec_a)
    norma_b = np.linalg.norm(vec_b)
    if norma_a == 0 or norma_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norma_a * norma_b))

def sim_rapida(a: np.ndarray, b: np.ndarray) -> float:
    """Atalho para vetores JÁ normalizados (norma = 1).
    O produto escalar de vetores com norma 1 é a similaridade cosseno.
    """
    return float(np.dot(a, b))

# ------------------------------------------------------------------------------
# 2.3 Busca em Um Conjunto de Vetores
# ------------------------------------------------------------------------------
def buscar_top_k(query_vec: np.ndarray, matriz: np.ndarray, k: int = 5) -> tuple[np.ndarray, np.ndarray]:
    """
    Busca os k vetores mais similares na matriz.
    Assume vetores normalizados (norma = 1).
    Retorna (índices, scores) em ordem decrescente.
    """
    # scores: shape (N,) — produto escalar de cada linha com query_vec
    scores = matriz @ query_vec 
    indices_top = np.argsort(scores)[::-1][:k]
    return indices_top, scores[indices_top]

if __name__ == "__main__":
    # Exemplo simples 2D
    a = np.array([1.0, 0.0]) # aponta para a direita
    b = np.array([1.0, 0.0]) # mesma direção
    c = np.array([0.0, 1.0]) # perpendicular
    d = np.array([-1.0, 0.0]) # direção oposta

    print("a vs b:", similaridade_cosseno(a, b)) # 1.0 — idênticos
    print("a vs c:", similaridade_cosseno(a, c)) # 0.0 — sem relação
    print("a vs d:", similaridade_cosseno(a, d)) # -1.0 — opostos
