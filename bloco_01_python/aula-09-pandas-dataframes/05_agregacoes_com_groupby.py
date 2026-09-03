# Aula 09 — Pandas I
# Capítulo 5: Agregações com groupby()

import pandas as pd

# =====================================================================
# DataFrame de Teste
# =====================================================================
df = pd.DataFrame({
    'nome': ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena', 'Fabio'],
    'turma': ['A', 'A', 'B', 'B', 'C', 'C'],
    'nota': [8.5, 6.0, 9.2, 4.5, 7.8, 5.5],
    'faltas': [1, 3, 0, 5, 2, 4],
})


# =====================================================================
# 5.1 Agregações Simples
# =====================================================================
print("--- 5.1 Agregações Simples ---")

# Média de nota agrupada por turma
print("-> Média das notas por turma:")
print(df.groupby('turma')['nota'].mean())

# Soma de faltas por turma
print("\n-> Soma de faltas por turma:")
print(df.groupby('turma')['faltas'].sum())

# Contagem de alunos por turma (tamanho do grupo)
print("\n-> Quantidade de alunos por turma:")
print(df.groupby('turma').size())

# Máximo e mínimo
print("\n-> Maior nota por turma:")
print(df.groupby('turma')['nota'].max())

print("\n-> Menor nota por turma:")
print(df.groupby('turma')['nota'].min())
print("\n")


# =====================================================================
# 5.2 agg() — Múltiplas Funções Simultâneas
# =====================================================================
print("--- 5.2 agg() — Múltiplas Funções ---")

# Múltiplas funções aplicadas à mesma coluna
resumo_nota = df.groupby('turma')['nota'].agg(['mean', 'min', 'max', 'count'])
print("-> Múltiplas estatísticas apenas para a coluna 'nota':")
print(resumo_nota.round(2))

# Funções diferentes para colunas diferentes (Muito poderoso!)
resumo_geral = df.groupby('turma').agg(
    media_nota = ('nota', 'mean'),
    total_faltas = ('faltas', 'sum'),
    n_alunos = ('nome', 'count'),
)
print("\n-> Estatísticas mistas (Renomeando e aplicando lógicas diferentes por coluna):")
print(resumo_geral.round(2))

# reset_index() — transforma o índice de grupo de volta em uma coluna normal da tabela
resumo_geral = resumo_geral.reset_index()
print("\n-> Após o reset_index() a turma volta a ser coluna, pronto pra outras operações:")
print(resumo_geral)
print("\n")


# =====================================================================
# 5.3 groupby com Múltiplas Colunas
# =====================================================================
print("--- 5.3 groupby com Múltiplas Colunas (Subgrupos) ---")

df_bim = pd.DataFrame({
    'turma': ['A','A','A','A','B','B','B','B'],
    'bimestre': ['1B','2B','1B','2B','1B','2B','1B','2B'],
    'aluno': ['Ana','Ana','Bruno','Bruno','Carla','Carla','Diego','Diego'],
    'nota': [8.0, 9.0, 6.0, 7.0, 9.5, 8.5, 4.0, 5.0],
})

# Agrupar por dois critérios: turma e DEPOIS bimestre
media_bim = (df_bim
    .groupby(['turma', 'bimestre'])['nota']
    .mean()
    .round(2)
    .reset_index()
    .rename(columns={'nota': 'media_nota'})
)
print("-> Média das notas separadas por Turma e por Bimestre:")
print(media_bim)

# Encadeamento completo: filtrar -> agrupar -> ordenar
print("\n-> Pipeline completo (Aprovados (>=5) -> Média por Turma -> Ordenado -> Reset Index):")
top = (df
    .query('nota >= 5.0')
    .groupby('turma')['nota']
    .mean()
    .round(2)
    .sort_values(ascending=False) # Ordem decrescente
    .reset_index()
)
print(top)
