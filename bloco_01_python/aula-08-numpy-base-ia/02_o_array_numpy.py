import numpy as np

# ==========================================
# 2.1 Criando Arrays
# ==========================================
print("--- 2.1 Criando Arrays ---")
# A partir de listas Python — conversão explícita
a = np.array([1, 2, 3, 4, 5])
print(a)         # [1 2 3 4 5]
print(type(a))   # <class 'numpy.ndarray'>

# Array 2D — lista de listas (matriz)
m = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print(m)
# [[1 2 3]
#  [4 5 6]
#  [7 8 9]]

# Arrays de zeros, uns e valores específicos
zeros = np.zeros(5)              # [0. 0. 0. 0. 0.]
uns   = np.ones((3, 4))          # matriz 3x4 de 1.0
cheio = np.full((2, 3), 7)       # matriz 2x3 de 7
identidade = np.eye(3)           # matriz identidade 3x3

# Sequências numéricas
seq = np.arange(0, 10, 2)        # [0 2 4 6 8] — como range()
lin = np.linspace(0, 1, 5)       # [0.   0.25 0.5  0.75 1.  ]
# linspace(inicio, fim, n): n pontos igualmente espaçados

# Arrays aleatórios — essenciais para IA (inicialização de pesos)
aleatorio = np.random.rand(3, 4)     # floats uniformes [0, 1)
normal    = np.random.randn(3, 4)    # distribuição normal (média 0, dp 1)
inteiros  = np.random.randint(0, 10, size=(3, 3)) # inteiros [0, 10)

# Semente para reprodutibilidade — sempre use em experimentos
np.random.seed(41)
print("Aleatório com seed:", np.random.rand(3))  # sempre o mesmo resultado


# ==========================================
# 2.2 Atributos Fundamentais: shape, ndim, size, dtype
# ==========================================
print("\n--- 2.2 Atributos Fundamentais: shape, ndim, size, dtype ---")
a = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0]])

print("shape:", a.shape)   # (2, 3) — 2 linhas, 3 colunas
print("ndim:", a.ndim)    # 2      — número de dimensões (eixos)
print("size:", a.size)    # 6      — total de elementos
print("dtype:", a.dtype)   # float64 — tipo de cada elemento

# Especificando dtype na criação
f32 = np.array([1, 2, 3], dtype=np.float32)
print("dtype especificado:", f32.dtype) # float32

# Convertendo dtype
inteiros = a.astype(np.int32)
print("dtype convertido:", inteiros.dtype) # int32
print(inteiros)
# [[1 2 3]
#  [4 5 6]]

# Tamanho em bytes
print("nbytes de a:", a.nbytes)       # 48 bytes (6 elementos × 8 bytes)
print("nbytes de f32:", f32.nbytes)     # 12 bytes (3 elementos × 4 bytes)


# ==========================================
# 2.3 Reshape: Mudando a Forma sem Copiar Dados
# ==========================================
print("\n--- 2.3 Reshape: Mudando a Forma sem Copiar Dados ---")
a = np.arange(12)      # [ 0  1  2  3  4  5  6  7  8  9 10 11]
print("shape original:", a.shape)         # (12,)

b = a.reshape(3, 4)    # 3 linhas, 4 colunas
print("shape após reshape(3, 4):", b.shape)         # (3, 4)
print(b)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

c = a.reshape(2, 2, 3) # tensor 3D: 2 blocos de matriz 2x3
print("shape após reshape(2, 2, 3):", c.shape)         # (2, 2, 3)

# -1 como dimensão: NumPy calcula automaticamente
d = a.reshape(4, -1)   # 4 linhas, NumPy calcula colunas = 3
print("shape após reshape(4, -1):", d.shape)         # (4, 3)

# flatten(): transforma qualquer array em 1D (cria cópia)
e = b.flatten()
print("flatten():", e)               # [ 0  1  2  3  4  5  6  7  8  9 10 11]

# ravel(): também 1D, mas prefere não copiar (mais eficiente)
f = b.ravel()
print("ravel() shape:", f.shape)         # (12,)
