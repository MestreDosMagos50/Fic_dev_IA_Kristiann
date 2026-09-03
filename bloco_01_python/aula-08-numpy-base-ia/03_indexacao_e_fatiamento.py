import numpy as np

# ==========================================
# 3.1 Arrays 1D
# ==========================================
print("--- 3.1 Arrays 1D ---")
a = np.array([10, 20, 30, 40, 50, 60])

# Indexação simples — igual a listas Python
print("Primeiro:", a[0])    # 10   (primeiro)
print("Último:", a[-1])   # 60   (último)

# Fatiamento: [início:fim:passo] — igual a listas
print("Fatia [1:4]:", a[1:4])  # [20 30 40]
print("Fatia de 2 em 2 [::2]:", a[::2])  # [10 30 50]
print("Array invertido [::-1]:", a[::-1]) # [60 50 40 30 20 10]

# DIFERENÇA IMPORTANTE vs listas: fatias são VIEWS, não cópias
# Modificar a fatia modifica o array original
print("\n--- Trabalhando com Fatias (Views vs Cópias) ---")
a = np.array([10, 20, 30, 40, 50, 60]) # Recriando para o exemplo
fatia = a[1:4]
fatia[0] = 999
print("Fatia modificada:", fatia)
print("Array original após modificar a fatia:", a)       # [ 10 999  30  40  50  60] — original alterado!

# Para ter uma cópia independente, use .copy()
copia = a[1:4].copy()
copia[0] = 0
print("\nUsando .copy() para ter cópia independente:")
print("Cópia modificada:", copia)
print("Array original NÃO é alterado:", a)       # original não é alterado


# ==========================================
# 3.2 Arrays 2D
# ==========================================
print("\n--- 3.2 Arrays 2D ---")
m = np.array([[1,  2,  3,  4],
              [5,  6,  7,  8],
              [9, 10, 11, 12]])

# shape: (3, 4) — 3 linhas, 4 colunas

# Indexação: m[linha, coluna]
print("Linha 0, Coluna 0:", m[0, 0])   # 1
print("Linha 1, Coluna 2:", m[1, 2])   # 7
print("Última linha, Última coluna:", m[-1, -1]) # 12

# Selecionar linha inteira
print("\nLinha 0 inteira:", m[0])      # [1 2 3 4]
print("Linha 1 inteira (com fatiamento):", m[1, :])   # [5 6 7 8]

# Selecionar coluna inteira
print("\nColuna 0 inteira:", m[:, 0])   # [1 5 9]
print("Coluna 2 inteira:", m[:, 2])   # [3 7 11]

# Submatriz (fatia 2D)
print("\nSubmatriz (m[0:2, 1:3]):")
print(m[0:2, 1:3])
# [[2 3]
#  [6 7]]

# Indexação booleana — seleciona elementos que satisfazem condição
# Fundamental para filtrar dados em pré-processamento
print("\n--- Indexação Booleana ---")
mask = m > 6
print("Máscara Booleana (m > 6):")
print(mask)
# [[False False False False]
#  [False False  True  True]
#  [ True  True  True  True]]

print("Valores maiores que 6 (m[mask]):", m[mask]) # [ 7  8  9 10 11 12]

# Fancy indexing — selecionar linhas específicas por índice
print("\n--- Fancy Indexing ---")
print("Selecionando linhas 0 e 2 (m[[0, 2]]):")
print(m[[0, 2]]) # linhas 0 e 2
# [[ 1  2  3  4]
#  [ 9 10 11 12]]
