import numpy as np

# ==========================================
# 5.1 Medidas Descritivas
# ==========================================
print("--- 5.1 Medidas Descritivas ---")
notas = np.array([[7.5, 8.0, 9.2, 6.8],   # aluno 1
                  [5.0, 6.5, 7.0, 8.5],   # aluno 2
                  [9.0, 9.5, 8.8, 10.0]]) # aluno 3
# shape: (3, 4) — 3 alunos, 4 provas

print("Notas da turma:\n", notas)

# Sobre o array inteiro (todos os 12 valores)
print("\nEstatísticas Gerais (sobre todos os 12 valores):")
print("Média Geral:", np.mean(notas))    # 8.025 — média geral
print("Desvio Padrão:", np.std(notas))     # 1.371 — desvio padrão
print("Variância:", np.var(notas))     # 1.880 — variância
print("Menor valor:", np.min(notas))     # 5.0   — menor valor
print("Maior valor:", np.max(notas))     # 10.0  — maior valor
print("Soma de todos:", np.sum(notas))     # 96.3  — soma de todos
print("Mediana:", np.median(notas))  # 8.25  — mediana

# ==========================================
# O conceito de "axis" (MUITO IMPORTANTE!)
# ==========================================
print("\n--- O conceito de 'axis' ---")
# axis=1: opera ao longo das colunas -> colapsa as colunas, restando os alunos
media_alunos = np.mean(notas, axis=1)
print("Média de cada aluno (axis=1):", media_alunos) # [7.875 6.75  9.325]

# axis=0: opera ao longo das linhas -> colapsa as linhas, restando as provas
media_provas = np.mean(notas, axis=0)
print("Média de cada prova (axis=0):", media_provas) # [7.167 8.    8.333 8.433]

# Percentis — extremamente úteis para detectar outliers
print("\nPercentis:")
print("1º Quartil (25%):", np.percentile(notas, 25)) 
print("Mediana (50%):", np.percentile(notas, 50)) 
print("3º Quartil (75%):", np.percentile(notas, 75)) 

# argmin / argmax — índice do menor/maior valor
print("\nÍndices de Mínimo e Máximo:")
print("Índice da menor nota por aluno (argmin axis=1):", np.argmin(notas, axis=1)) # [3 0 0]
print("Índice da maior nota por aluno (argmax axis=1):", np.argmax(notas, axis=1)) # [2 3 3]

# Funções de array como métodos (equivalentes)
print("\nFunções de array como métodos:")
print("notas.mean():", notas.mean())         # igual a np.mean(notas)
print("notas.std():", notas.std())          # igual a np.std(notas)
print("notas.sum(axis=0):", notas.sum(axis=0))    # igual a np.sum(notas, axis=0)
