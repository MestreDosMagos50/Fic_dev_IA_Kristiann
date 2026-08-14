import numpy as np

# ==========================================
# 7. O que é um Tensor — Intuição para IA
# ==========================================
print("--- 7.1 A Hierarquia de Dimensões ---")

# ── Escalar — tensor de ordem 0 (0 dimensões) ────────────
escalar = np.array(42.0)
print("\nEscalar:")
print("Shape:", escalar.shape) # () — sem dimensões
print("Ndim:", escalar.ndim) # 0
# Representa: um único número — uma temperatura, uma probabilidade

# ── Vetor — tensor de ordem 1 (1 dimensão) ───────────────
vetor = np.array([0.2, 0.5, 0.8, 0.1, 0.9])
print("\nVetor:")
print("Shape:", vetor.shape) # (5,) — 5 elementos
print("Ndim:", vetor.ndim) # 1
# Representa: embedding de uma palavra, features de um exemplo, pesos

# ── Matriz — tensor de ordem 2 (2 dimensões) ─────────────
matriz = np.random.rand(128, 768)
print("\nMatriz:")
print("Shape:", matriz.shape) # (128, 768)
print("Ndim:", matriz.ndim) # 2
# Representa: batch de 128 embeddings de 768 dimensões cada (padrão BERT/GPT)

# ── Tensor 3D — tensor de ordem 3 ────────────────────────
tensor3d = np.random.rand(32, 64, 64)
print("\nTensor 3D:")
print("Shape:", tensor3d.shape) # (32, 64, 64)
print("Ndim:", tensor3d.ndim) # 3
# Representa: batch de 32 imagens em escala de cinza 64x64

# ── Tensor 4D — tensor de ordem 4 ────────────────────────
tensor4d = np.random.rand(32, 3, 64, 64)
print("\nTensor 4D:")
print("Shape:", tensor4d.shape) # (32, 3, 64, 64)
print("Ndim:", tensor4d.ndim) # 4
# Representa: batch de 32 imagens RGB (3 canais) 64x64
# Formato padrão em IA: (batch, canais, altura, largura)


print("\n--- 7.2 Por que Tensores Importam para IA ---")
# ── Exemplo: como um texto vira tensor ───────────────────

# 1. Texto bruto
texto = "Python é essencial para IA"
print(f"1. Texto Bruto: '{texto}'")

# 2. Tokenização simples (em LLMs reais, usam tokenizadores treinados)
tokens = texto.lower().split() 
print(f"2. Tokens: {tokens}")

# 3. Embedding: cada token vira um vetor de floats
np.random.seed(42)
dim_embedding = 8
embeddings = {token: np.random.randn(dim_embedding) for token in tokens}

# 4. Sequência de embeddings -> tensor 2D
sequencia = np.array([embeddings[t] for t in tokens])
print(f"4. Sequência de embeddings (Shape): {sequencia.shape} — {sequencia.shape[0]} tokens de {sequencia.shape[1]} dimensões")

# 5. Com batch processing -> tensor 3D
batch = sequencia[np.newaxis, :, :] # Adiciona uma nova dimensão no início (batch)
print(f"5. Com Batch Processing (Shape 3D): {batch.shape}")
