# Aula 09 — Pandas I
# Capítulo 2: Seleção de Colunas e Linhas

import pandas as pd

# =====================================================================
# DataFrame de Teste (Criado na Aula 1.1)
# =====================================================================
df = pd.DataFrame({
    'nome': ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena'],
    'turma': ['A', 'A', 'B', 'B', 'C'],
    'idade': [20, 22, 21, 23, 20],
    'nota': [8.5, 6.0, 9.2, 4.5, 7.8],
})


# =====================================================================
# 2.1 Selecionando Colunas
# =====================================================================
print("--- 2.1 Selecionando Colunas ---")

# Uma coluna retorna uma Series
nomes = df['nome']
print("-> Tipo ao selecionar uma única coluna df['nome']:")
print(type(nomes)) # <class 'pandas.core.series.Series'>

# Múltiplas colunas retornam um DataFrame (precisa de uma LISTA dentro dos colchetes)
df_sub = df[['nome', 'nota', 'turma']]
print("\n-> Tipo ao selecionar múltiplas colunas df[['nome', 'nota', 'turma']]:")
print(type(df_sub)) # <class 'pandas.core.frame.DataFrame'>
print(df_sub)

# ERRO comum comentado para não quebrar o código:
# erro = df['nome', 'nota'] # Retorna KeyError porque tentou buscar uma tupla e não uma lista
print("\n")


# =====================================================================
# 2.2 loc[] — Seleção por Rótulo (Label)
# =====================================================================
print("--- 2.2 loc[] — Seleção por Rótulo ---")

# Linha por rótulo de índice
print("-> df.loc[0]:")
print(df.loc[0]) # linha com índice 0 → Retorna uma Series

print("\n-> df.loc[2]:")
print(df.loc[2]) # linha com índice 2

# Intervalo de rótulos (INCLUSIVO nos dois extremos - diferente das listas normais do Python!)
print("\n-> df.loc[1:3] (Linhas 1, 2 e 3):")
print(df.loc[1:3])

# Linha + coluna (Cruzamento)
print("\n-> df.loc[0, 'nome']:")
print(df.loc[0, 'nome']) # Retorna 'Ana'

# Múltiplas linhas + múltiplas colunas
print("\n-> df.loc[0:2, ['nome', 'nota']]:")
print(df.loc[0:2, ['nome', 'nota']])

# Todas as linhas (:), de uma coluna específica
print("\n-> df.loc[:, 'nota']:")
print(df.loc[:, 'nota'])
print("\n")


# =====================================================================
# 2.3 iloc[] — Seleção por Posição Inteira
# =====================================================================
print("--- 2.3 iloc[] — Seleção por Posição Inteira ---")
print("AVISO: O iloc é como índices de listas no Python. O limite final é EXCLUSIVO (não entra).")

# Linha por posição
print("\n-> df.iloc[0]:")
print(df.iloc[0]) # primeira linha

print("\n-> df.iloc[-1]:")
print(df.iloc[-1]) # última linha (igual em listas)

# Intervalo de posições (exclusivo no fim, como range())
print("\n-> df.iloc[1:3] (Não inclui a linha 3!):")
print(df.iloc[1:3]) # posições 1 e 2 

# Linha + coluna por posição (Cruzamento usando apenas os números)
print("\n-> df.iloc[0, 0]:")
print(df.iloc[0, 0]) # primeira célula: 'Ana'

# Últimas 2 linhas, primeiras 3 colunas
print("\n-> df.iloc[-2:, :3]:")
print(df.iloc[-2:, :3])

# Posições não-contíguas com lista de listas
print("\n-> df.iloc[[0, 2, 4], [0, 3]] (Linhas 0, 2, 4 e Colunas 0, 3):")
print(df.iloc[[0, 2, 4], [0, 3]])
