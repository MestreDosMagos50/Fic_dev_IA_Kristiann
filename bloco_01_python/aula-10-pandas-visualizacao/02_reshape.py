import pandas as pd

print("2. Reestruturando DataFrames: Reshape\n")

print("--- 2.1 pivot_table(): do Formato Longo para o Largo ---\n")

# DataFrame em formato longo (tidy data)
avaliacoes = pd.DataFrame({
    'aluno': ['Ana','Ana','Ana','Bruno','Bruno','Bruno'],
    'disciplina': ['Mat','Port','Hist','Mat','Port','Hist'],
    'nota': [8.5, 7.5, 9.0, 7.0, 8.5, 6.5],
})

print("DataFrame Original (Formato Longo):")
print(avaliacoes)

# pivot_table: disciplinas viram colunas, notas ficam nos valores
tabela_larga = avaliacoes.pivot_table(
    values='nota',        # coluna com os valores
    index='aluno',        # coluna que vira índice (linhas)
    columns='disciplina', # coluna cujos valores viram colunas
    aggfunc='mean',       # função de agregação (padrão: mean)
)

print("\nResultado do pivot_table (Formato Largo):")
print(tabela_larga)

# Redefinindo o índice para facilitar operações posteriores
tabela_larga = tabela_larga.reset_index()
tabela_larga.columns.name = None # remove o nome 'disciplina' do cabeçalho
print("\nResultado após reset_index e remover o nome das colunas:")
print(tabela_larga)


print("\n\n--- 2.2 melt(): do Formato Largo para o Longo ---\n")

# DataFrame em formato largo (uma coluna por disciplina)
notas_largas = pd.DataFrame({
    'aluno': ['Ana', 'Bruno', 'Carla'],
    'matematica': [8.5, 7.0, 9.0],
    'portugues': [7.5, 8.5, 6.0],
    'historia': [9.0, 6.5, 8.0],
})

print("DataFrame Original (Formato Largo):")
print(notas_largas)

# melt: transforma colunas de disciplinas em linhas
notas_longas = notas_largas.melt(
    id_vars='aluno',           # coluna(s) que permanecem fixas
    var_name='disciplina',     # nome da nova coluna de categorias
    value_name='nota',         # nome da nova coluna de valores
)

print("\nResultado do melt (Formato Longo):")
print(notas_longas.head(6))
