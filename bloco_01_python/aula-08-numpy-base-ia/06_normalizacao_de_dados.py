import numpy as np

# ==========================================
# 6.1 Normalização Min-Max (Escala [0, 1])
# ==========================================
print("--- 6.1 Normalização Min-Max (Escala [0, 1]) ---")
# Fórmula: x_norm = (x - x_min) / (x_max - x_min)

dados = np.array([20.0, 35.0, 50.0, 80.0, 100.0])
print("Dados originais:", dados)

x_min = dados.min()
x_max = dados.max()
dados_norm = (dados - x_min) / (x_max - x_min)
print("Dados Min-Max:", dados_norm) # [0.     0.1875 0.375  0.75   1.    ]

# Verificação: min deve ser 0, max deve ser 1
print("Verificação - Min:", dados_norm.min()) # 0.0
print("Verificação - Max:", dados_norm.max()) # 1.0

# Função reutilizável com type hints e docstring
def normalizar_minmax(arr: np.ndarray) -> np.ndarray:
    """Normaliza um array para o intervalo [0, 1]."""
    x_min = arr.min()
    x_max = arr.max()
    if x_max == x_min:
        return np.zeros_like(arr, dtype=float)
    return (arr - x_min) / (x_max - x_min)

# Aplicando em matriz (normaliza cada coluna independentemente)
print("\n--- Normalizando uma Matriz ---")
matriz = np.array([[10.0, 200.0],
                   [30.0, 400.0],
                   [50.0, 600.0]])
print("Matriz original:\n", matriz)

# axis=0: min/max por coluna, resultado esticado por broadcasting
col_min = matriz.min(axis=0) # [10. 200.]
col_max = matriz.max(axis=0) # [50. 600.]
normalizada = (matriz - col_min) / (col_max - col_min)
print("Matriz Min-Max (por coluna):\n", normalizada)


# ==========================================
# 6.2 Padronização Z-Score (Média 0, Desvio Padrão 1)
# ==========================================
print("\n--- 6.2 Padronização Z-Score ---")
# Fórmula: x_pad = (x - média) / desvio_padrão

media = dados.mean()
dp = dados.std()
print(f"Média original: {media:.2f}")
print(f"Desvio padrão original: {dp:.2f}")

dados_pad = (dados - media) / dp
print("Dados Padronizados (Z-Score):", dados_pad.round(3))
# [-1.299 -0.719 -0.14   0.891  1.267]

# Verificação: média ≈ 0, desvio padrão ≈ 1
print(f"Verificação - Média padronizada: {dados_pad.mean():.10f}") # ~0
print(f"Verificação - Desvio padronizado: {dados_pad.std():.4f}")  # 1.0

def padronizar_zscore(arr: np.ndarray) -> np.ndarray:
    """Padroniza um array para média 0 e desvio padrão 1."""
    dp = arr.std()
    if dp == 0:
        return np.zeros_like(arr, dtype=float)
    return (arr - arr.mean()) / dp

# Padronizando colunas de uma matriz independentemente
print("\n--- Padronizando uma Matriz ---")
media_col = matriz.mean(axis=0) # média de cada coluna
dp_col = matriz.std(axis=0)     # dp de cada coluna
padronizada_z = (matriz - media_col) / dp_col
print("Matriz Z-Score (por coluna):\n", padronizada_z.round(3))
