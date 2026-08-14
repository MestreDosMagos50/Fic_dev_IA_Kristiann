# Aula 09 — Pandas I
# Capítulo 4: Valores Ausentes (Missing Values)

import pandas as pd
import numpy as np

# =====================================================================
# 4.1 Detectando Valores Ausentes
# =====================================================================
print("--- 4.1 Detectando Valores Ausentes ---")

# DataFrame com valores ausentes simulados
df_missing = pd.DataFrame({
    'nome': ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena'],
    'nota': [8.5, np.nan, 9.2, np.nan, 7.8],
    'turma': ['A', 'A', None, 'B', 'C'],
    'idade': [20, 22, 21, np.nan, 20],
})

print("-> DataFrame com dados faltando (NaN / None):")
print(df_missing)

# isna() / isnull() — retorna DataFrame booleano
print("\n-> df.isna() (Quais células estão vazias?):")
print(df_missing.isna())

# Contar NaN por coluna — imprescindível na inspeção inicial
print("\n-> Contagem de NaN por coluna (MUITO ÚTIL):")
print(df_missing.isna().sum())

# Percentual de ausentes
percentual = (df_missing.isna().sum() / len(df_missing) * 100).round(1)
print("\n-> Percentual de ausentes por coluna (%):")
print(percentual)

# Verificar se há ALGUM NaN em qualquer lugar
print("\n-> Há algum dado faltando na tabela inteira?")
print(df_missing.isna().any().any()) 
print("\n")


# =====================================================================
# 4.2 dropna() — Remover Linhas ou Colunas com NaN
# =====================================================================
print("--- 4.2 dropna() — Removendo Ausentes ---")

# Remover linhas com QUALQUER NaN (padrão)
df_limpo = df_missing.dropna()
print("-> Removendo linhas com QUALQUER valor NaN:")
print(df_limpo)
print(f"Formato original: {df_missing.shape} | Após dropna(): {df_limpo.shape}")

# Remover apenas linhas em que TODAS as colunas são NaN
df_limpo_todas = df_missing.dropna(how='all')

# Remover apenas se NaN em colunas específicas
df_limpo_subset = df_missing.dropna(subset=['nota', 'turma'])

# Exigir mínimo de N valores não-nulos por linha
df_limpo_thresh = df_missing.dropna(thresh=3) # mínimo 3 valores preenchidos na linha

# Remover colunas inteiras com NaN (axis=1) em vez de linhas
df_sem_col_nan = df_missing.dropna(axis=1)
print("\n-> Removendo COLUNAS inteiras que possuem qualquer NaN (axis=1):")
print(df_sem_col_nan)
print("\n")


# =====================================================================
# 4.3 fillna() — Preencher Valores Ausentes
# =====================================================================
print("--- 4.3 fillna() — Preenchendo Ausentes ---")

# Copiando para não estragar o original
df_filled = df_missing.copy()

# Preencher a tabela toda com um valor fixo
df_zero = df_missing.fillna(0) 

# Preencher com a média da coluna (estratégia mais comum para numéricas)
media_nota = df_missing['nota'].mean()
df_filled['nota'] = df_missing['nota'].fillna(media_nota)
print(f"-> Média das notas calculada para preencher os buracos: {media_nota:.2f}")

# Preencher com mediana (mais robusta a outliers)
mediana_idade = df_missing['idade'].median()
df_filled['idade'] = df_missing['idade'].fillna(mediana_idade)

# Preencher com um texto fixo em colunas categóricas
df_filled['turma'] = df_missing['turma'].fillna('Desconhecido')

print("\n-> DataFrame final com os buracos preenchidos:")
print(df_filled)

# Outras formas úteis (comentadas como referência):
# Preencher com o valor anterior (forward fill) — muito útil em séries temporais (ações, clima)
# df_ffill = df_missing.ffill()

# Preencher com o valor seguinte (backward fill)
# df_bfill = df_missing.bfill()

# Preencher colunas diferentes com valores diferentes em um único comando
# dicionario_preenchimento = {
#     'nota': df_missing['nota'].mean(),
#     'turma': 'Não informado',
#     'idade': df_missing['idade'].median(),
# }
# df_multi = df_missing.fillna(dicionario_preenchimento)
