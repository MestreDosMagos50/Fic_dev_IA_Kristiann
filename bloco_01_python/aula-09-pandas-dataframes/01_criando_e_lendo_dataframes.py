# Aula 09 — Pandas I
# Capítulo 1: Criando e Lendo DataFrames

import pandas as pd

# =====================================================================
# 1.1 Criação a partir de Dicionário
# =====================================================================
print("--- 1.1 Criação a partir de Dicionário ---")
# Cada chave vira uma coluna; as listas devem ter o mesmo comprimento
df = pd.DataFrame({
    'nome': ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena'],
    'turma': ['A', 'A', 'B', 'B', 'C'],
    'idade': [20, 22, 21, 23, 20],
    'nota': [8.5, 6.0, 9.2, 4.5, 7.8],
})
print(df)
print("\n")


# =====================================================================
# 1.2 Lendo CSV e Excel
# =====================================================================
print("--- 1.2 Lendo CSV e Excel ---")

# Ler CSV — o caso mais comum em projetos de dados
df_csv = pd.read_csv('vendas.csv', sep=';', encoding='utf-8')
print("--- Dados do CSV ---")
print(df_csv.head())

# Parâmetros úteis do read_csv (exemplo)
# df_csv = pd.read_csv('vendas.csv',
#     sep=';',           # separador (padrão: vírgula)
#     decimal='.',       # separador decimal
#     encoding='utf-8',
#     nrows=1000,        # ler apenas as primeiras N linhas
#     usecols=['Produto', 'Valor', 'Cliente'], # apenas estas colunas
# )

# Ler Excel
df_excel = pd.read_excel('vendas.xlsx', sheet_name='Planilha1')
print("\n--- Dados do Excel ---")
print(df_excel.head())

# Salvar de volta
df_csv.to_csv('resultado.csv', index=False, encoding='utf-8')
df_excel.to_excel('resultado.xlsx', index=False)
print("\nArquivos resultado.csv e resultado.xlsx gerados com sucesso!")
print("\n")


# =====================================================================
# 1.3 Inspeção Inicial — Comandos Essenciais
# =====================================================================
print("--- 1.3 Inspeção Inicial — Comandos Essenciais ---")
print("Sempre execute df.info() como primeiro passo ao carregar dados novos.\n")

# Para a inspeção, vamos usar o 'df' (tabela de alunos) que criamos lá em cima no 1.1
print("-> df.shape:")
print(df.shape)  # (5, 4) — linhas × colunas

print("\n-> df.dtypes:")
print(df.dtypes) # tipo de cada coluna

print("\n-> df.info():")
print(df.info()) # shape + dtypes + valores não-nulos

print("\n-> df.describe():")
print(df.describe()) # estatísticas das colunas numéricas

print("\n-> df.head(3):")
print(df.head(3)) # primeiras 3 linhas

print("\n-> df.tail(3):")
print(df.tail(3)) # últimas 3 linhas

print("\n-> df.columns.tolist():")
print(df.columns.tolist()) # lista de nomes de colunas

print("\n-> df.index:")
print(df.index) # índice (padrão: RangeIndex 0..N-1)

# Contar valores únicos por coluna categórica
print("\n-> df['turma'].value_counts():")
print(df['turma'].value_counts())
