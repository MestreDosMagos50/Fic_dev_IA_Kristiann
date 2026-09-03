import pandas as pd
import os
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split

print("4. Preparando o Dataset para Modelagem e IA\n")

print("--- 4.2 Codificação de Variáveis Categóricas ---\n")

df = pd.DataFrame({
    'aluno': ['Ana', 'Bruno', 'Carla', 'Diego', 'Elena'],
    'turma': ['A', 'B', 'A', 'C', 'B'],
    'situacao': ['Aprovado', 'Reprovado', 'Aprovado', 'Aprovado', 'Reprovado'],
    'media': [8.5, 5.5, 7.8, 7.2, 6.0],
    'faltas': [2, 10, 3, 1, 8]
})

print("DataFrame Original:")
print(df)

# --- Opção 1: One-Hot Encoding com pd.get_dummies() ---
# Cria uma coluna binária (0/1) para cada categoria
df_encoded = pd.get_dummies(df, columns=['turma'], prefix='turma', dtype=int)
print("\nColunas após One-Hot Encoding (pd.get_dummies):")
print(df_encoded.columns.tolist())

# --- Opção 2: Label Encoding manual ---
# Mapeia categorias para inteiros
df_encoded['situacao_num'] = df_encoded['situacao'].map({
    'Reprovado': 0,
    'Aprovado': 1,
})

# Removendo coluna de texto original e do aluno (o modelo não aceita texto)
df_encoded = df_encoded.drop(columns=['aluno', 'situacao'])
print("\nDataFrame após Label Encoding e remoção de texto:")
print(df_encoded.head())


print("\n--- 4.3 Normalização de Variáveis Numéricas ---\n")

colunas_numericas = ['media', 'faltas']

# --- StandardScaler: média 0, desvio padrão 1 ---
scaler_std = StandardScaler()
df_scaled = df_encoded.copy()
df_scaled[colunas_numericas] = scaler_std.fit_transform(df_encoded[colunas_numericas])

print("Descrição dos dados com StandardScaler (média ~ 0.0, std ~ 1.0):")
print(df_scaled[colunas_numericas].describe().round(3))

# --- MinMaxScaler: escala para o intervalo [0, 1] ---
scaler_mm = MinMaxScaler()
df_minmax = df_encoded.copy()
df_minmax[colunas_numericas] = scaler_mm.fit_transform(df_encoded[colunas_numericas])

print("\nDescrição dos dados com MinMaxScaler (min = 0.0, max = 1.0):")
print(df_minmax[colunas_numericas].describe().round(3))


print("\n--- 4.4 Separação Treino e Teste ---\n")

# Definindo features (X) e variável alvo (y)
X = df_scaled.drop(columns=['situacao_num']) # tudo menos o alvo
y = df_scaled['situacao_num']                # variável a ser prevista

# Divisão 80% treino / 20% teste
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y,
    test_size=0.40,     # Ajustado para 0.40 pois com 5 linhas precisamos de pelo menos 2 no teste para o stratify funcionar
    random_state=42,    # semente aleatória para reprodutibilidade
    stratify=y          # garante mesma proporção de classes nos dois conjuntos
)

print(f'Tamanho do Conjunto de Treino: {X_treino.shape[0]} amostras')
print(f'Tamanho do Conjunto de Teste: {X_teste.shape[0]} amostras')

# Criar diretório para salvar os datasets
os.makedirs('datasets', exist_ok=True)

# Salvando os conjuntos para uso posterior
X_treino.to_csv('datasets/X_treino.csv', index=False)
X_teste.to_csv('datasets/X_teste.csv', index=False)
y_treino.to_csv('datasets/y_treino.csv', index=False)
y_teste.to_csv('datasets/y_teste.csv', index=False)

print("\nDatasets salvos na pasta 'datasets/': X_treino.csv, X_teste.csv, y_treino.csv, y_teste.csv")
