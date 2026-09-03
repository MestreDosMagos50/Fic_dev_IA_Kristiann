import numpy as np

# ==========================================
# 4.1 Aritmética Elemento a Elemento
# ==========================================
print("--- 4.1 Aritmética Elemento a Elemento ---")
a = np.array([1.0, 2.0, 3.0, 4.0])
b = np.array([10.0, 20.0, 30.0, 40.0])

# Operações entre arrays — aplicadas elemento a elemento
print("a + b:", a + b)       # [11. 22. 33. 44.]
print("b - a:", b - a)       # [ 9. 18. 27. 36.]
print("a * b:", a * b)       # [ 10. 40. 90. 160.]
print("b / a:", b / a)       # [10. 10. 10. 10.]
print("a ** 2:", a ** 2)      # [ 1. 4. 9. 16.]

# Operações com escalares — aplicadas a todos os elementos
print("\nOperações com Escalares:")
print("a * 3:", a * 3)       # [3. 6. 9. 12.]
print("a + 100:", a + 100)     # [101. 102. 103. 104.]
print("a / 2:", a / 2)       # [0.5 1. 1.5 2. ]

# Comparação com loop Python equivalente (mais lento):
# resultado = [a[i] * b[i] for i in range(len(a))]
# NumPy faz isso em C — sem overhead do interpretador Python

# Operações de comparação — retornam array booleano
print("\nOperações de Comparação:")
print("a > 2:", a > 2)       # [False False True True]
print("a == 2:", a == 2)      # [False True False False]

# Operações lógicas em arrays
mask1 = a > 1
mask2 = a < 4
print("\nOperações Lógicas:")
print("mask1 & mask2 (e lógico):", mask1 & mask2) # [False True True False]
print("mask1 | mask2 (ou lógico):", mask1 | mask2) # [ True True True True]


# ==========================================
# 4.2 Broadcasting
# ==========================================
print("\n--- 4.2 Broadcasting ---")
# Regra básica: dimensões são comparadas da direita para a esquerda.
# São compatíveis se são iguais OU se uma delas é 1.

# Exemplo 1: matriz (3,4) + vetor (4,)
m = np.ones((3, 4))             # shape (3, 4)
v = np.array([1, 2, 3, 4])      # shape (4,)
print("Shape de (m + v):", (m + v).shape) # (3, 4) — v é 'esticado' para 3 linhas
print("m + v:\n", m + v)

# Exemplo 2: coluna (3,1) + linha (1,4)
col = np.array([[1], [2], [3]]) # shape (3, 1)
lin = np.array([[10, 20, 30, 40]]) # shape (1, 4)
print("\nShape de (col + lin):", (col + lin).shape) # (3, 4)
print("col + lin:\n", col + lin)

# Caso prático: centralizar cada coluna de uma matriz
print("\nCaso prático: centralizando colunas:")
dados = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]], dtype=float)

medias_colunas = dados.mean(axis=0)       # shape (3,)
centralizado = dados - medias_colunas     # broadcasting (3,3) - (3,)
print("Dados centralizados:\n", centralizado)


# ==========================================
# 4.3 Funções Universais (ufuncs)
# ==========================================
print("\n--- 4.3 Funções Universais (ufuncs) ---")
a = np.array([1.0, 4.0, 9.0, 16.0, 25.0])

# Funções matemáticas elementares
print("sqrt(a):", np.sqrt(a))
print("square(a):", np.square(a))
print("abs([-3, -1, 0, 2, 4]):", np.abs(np.array([-3, -1, 0, 2, 4])))

# Logaritmos e exponencial
print("\nLogaritmos e Exponenciais:")
print("log(a) [natural]:", np.log(a))
print("log2(a):", np.log2(a))
print("log10(a):", np.log10(a))
print("exp([0, 1, 2]):", np.exp(np.array([0, 1, 2])))

# Trigonometria (ângulos em radianos)
print("\nTrigonometria:")
angulos = np.linspace(0, np.pi, 5)
print("sin(angulos).round(3):", np.sin(angulos).round(3))
print("cos(angulos).round(3):", np.cos(angulos).round(3))

# Funções de arredondamento
print("\nArredondamento:")
x = np.array([1.2, 2.5, 3.7, 4.1])
print("round(x, 0):", np.round(x, 0))
print("floor(x):", np.floor(x))
print("ceil(x):", np.ceil(x))

# Clipping — limitar valores a um intervalo
# Muito usado para evitar overflow em ativações de redes neurais
print("\nClipping:")
y = np.array([-2, 0, 0.5, 1.5, 3])
print("clip(y, 0, 1):", np.clip(y, 0, 1))
