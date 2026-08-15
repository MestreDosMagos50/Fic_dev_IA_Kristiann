import pandas as pd

print("1. Combinando DataFrames: Merge e Join\n")

# --- Criando os DataFrames de exemplo ---
cadastro = pd.DataFrame({
    'id_aluno': [1, 2, 3, 4, 5],
    'nome': ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena'],
    'turma': ['A', 'A', 'B', 'B', 'C'],
})

notas = pd.DataFrame({
    'id_aluno': [1, 2, 3, 4, 6],    # aluno 5 ausente, aluno 6 extra
    'matematica': [8.5, 7.0, 9.0, 5.5, 8.0],
    'portugues': [7.5, 8.5, 6.0, 7.0, 9.5],
})

print("DataFrame 'cadastro':")
print(cadastro)
print("\nDataFrame 'notas':")
print(notas)

print("\n--- 1.1 Os Quatro Tipos de Join ---\n")

# --- Inner Join (padrão): apenas alunos presentes nos dois DataFrames ---
df_inner = pd.merge(cadastro, notas, on='id_aluno', how='inner')
print("Inner Join (interseção):")
print(df_inner)
# Resultado: 4 linhas (id 1,2,3,4). Aluno 5 e aluno 6 excluídos.

# --- Left Join: mantém todos do cadastro ---
df_left = pd.merge(cadastro, notas, on='id_aluno', how='left')
print("\nLeft Join (tabela da esquerda):")
print(df_left)
# Resultado: 5 linhas. Elena (id 5) tem NaN em matematica e portugues.

# --- Outer Join: mantém todos ---
df_outer = pd.merge(cadastro, notas, on='id_aluno', how='outer')
print("\nOuter Join (união):")
print(df_outer)
# Resultado: 6 linhas. Elena tem NaN em notas; aluno 6 tem NaN em nome e turma.


print("\n--- 1.2 Merge com Colunas de Nomes Diferentes ---\n")

frequencias = pd.DataFrame({
    'matricula': [1, 2, 3, 4, 5],  # mesmo significado que 'id_aluno'
    'faltas': [2, 0, 5, 1, 3],
})

# Merge com chaves de nomes diferentes
df_completo = pd.merge(
    cadastro,
    frequencias,
    left_on='id_aluno',      # coluna-chave no DataFrame da esquerda
    right_on='matricula',    # coluna-chave no DataFrame da direita
    how='left'
)

# Removendo a coluna duplicada (matricula é igual a id_aluno)
df_completo = df_completo.drop(columns=['matricula'])
print("Merge com chaves diferentes (após remover coluna duplicada 'matricula'):")
print(df_completo.head())


print("\n--- 1.3 Merge Encadeado: Combinando Três DataFrames ---\n")

# Combinando cadastro + notas + frequencias em um único DataFrame
df_final = (cadastro
    .merge(notas, on='id_aluno', how='left')
    .merge(frequencias, left_on='id_aluno', right_on='matricula', how='left')
    .drop(columns=['matricula'])
)

print("DataFrame Final após merges encadeados:")
print(df_final)
print("\nShape do DataFrame final:", df_final.shape)  # (5, 6): 5 alunos, 6 colunas

print("\nTipos de dados do DataFrame final:")
print(df_final.dtypes)

print("\nQuantidade de valores nulos (NaN) após o merge:")
print(df_final.isnull().sum())  # verificar NaN após o merge
