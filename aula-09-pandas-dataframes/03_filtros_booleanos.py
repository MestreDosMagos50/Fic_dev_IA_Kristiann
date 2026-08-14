# Aula 09 — Pandas I
# Capítulo 3: Filtros Booleanos

import pandas as pd
import numpy as np

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
# 3.1 Filtros Simples
# =====================================================================
print("--- 3.1 Filtros Simples ---")

# Condição simples retorna uma "máscara" booleana (True/False para cada linha)
mask = df['nota'] >= 7.0
print("-> Máscara booleana para notas >= 7.0:")
print(mask)

# Aplicar o filtro (passando a máscara para dentro do DataFrame)
aprovados = df[df['nota'] >= 7.0]
print("\n-> Aplicando o filtro (aprovados):")
print(aprovados)

# Filtro por valor de string
turma_a = df[df['turma'] == 'A']
print("\n-> Filtro por string (apenas turma A):")
print(turma_a)

# Filtro com isin() — equivalente ao IN do SQL
turmas_ab = df[df['turma'].isin(['A', 'B'])]
print("\n-> Filtro com isin (Turmas A ou B):")
print(turmas_ab)
print("\n")


# =====================================================================
# 3.2 Filtros Compostos
# =====================================================================
print("--- 3.2 Filtros Compostos ---")
print("AVISO: Sempre use parênteses () em cada condição antes do & ou |.")

# E / AND (ambas as condições devem ser verdadeiras -> usamos & )
aprovados_a = df[(df['nota'] >= 7.0) & (df['turma'] == 'A')]
print("\n-> Filtro E (&): Aprovados DA turma A:")
print(aprovados_a)

# OU / OR (pelo menos uma condição verdadeira -> usamos | )
extremos = df[(df['nota'] >= 9.0) | (df['nota'] < 5.0)]
print("\n-> Filtro OU (|): Notas extremas (>=9.0 ou <5.0):")
print(extremos)

# Negação / NOT (inverte o filtro -> usamos ~ )
nao_turma_b = df[~(df['turma'] == 'B')]
print("\n-> Filtro de Negação (~): Todos que NÃO são da turma B:")
print(nao_turma_b)

# ERRO clássico (sem parênteses). O Python tentaria processar o & antes do >=
# df[df['nota'] >= 7.0 & df['turma'] == 'A']  # Isso causaria TypeError!

# query() — alternativa muito mais legível para condições como se fosse SQL
aprovados_query = df.query('nota >= 7.0 and turma == "A"')
print("\n-> Filtro usando .query():")
print(aprovados_query)

# Filtro com between()
medios = df[df['nota'].between(6.0, 8.0)]
print("\n-> Filtro com .between(6.0, 8.0):")
print(medios)
print("\n")


# =====================================================================
# 3.3 Criando Colunas Derivadas
# =====================================================================
print("--- 3.3 Criando Colunas Derivadas ---")

# Criando uma coluna booleana simples a partir de uma condição
df['aprovado'] = df['nota'] >= 7.0

# Coluna categórica com np.where (Funciona como um IF/ELSE rápido)
# Se a condição for True -> 'Aprovado', Se for False -> 'Reprovado'
df['situacao'] = np.where(df['nota'] >= 7.0, 'Aprovado', 'Reprovado')

# Coluna com apply() — útil para regras mais complexas com funções customizadas
def classificar(nota):
    if nota >= 9.0: return 'Excelente'
    if nota >= 7.0: return 'Aprovado'
    if nota >= 5.0: return 'Recuperação'
    return 'Reprovado'

# Passamos a função (sem parênteses) para o apply() rodar linha a linha
df['conceito'] = df['nota'].apply(classificar)

# Operações matemáticas entre colunas (criando nota normalizada de 0 a 1)
df['nota_normalizada'] = (df['nota'] - df['nota'].min()) / \
                         (df['nota'].max() - df['nota'].min())

print("-> DataFrame final com as novas colunas geradas:")
print(df)
