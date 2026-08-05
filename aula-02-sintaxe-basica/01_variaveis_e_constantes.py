# 01_variaveis_e_constantes.py
# Aula 02: Sintaxe Essencial e Tipos Básicos

# --- 1. Variáveis e Convenções PEP 8 ---
# Variáveis e funções usam snake_case (todas minúsculas separadas por underline)
nome_completo = "Maria Silva"
idade_usuario = 25
preco_produto = 49.90
produto_disponivel = True

# --- 2. Constantes ---
# Por convenção PEP 8, constantes usam SCREAMING_SNAKE_CASE (tudo maiúsculo)
TAXA_IMPOSTO = 0.15          # 15% de imposto
VELOCIDADE_LUZ = 299_792_458 # m/s (underlines para facilitar a leitura de números grandes)
PI = 3.14159265358979

# --- 3. Múltiplas Atribuições ---
x, y, z = 10, 20, 30
a = b = c = 0

# --- 4. Verificando Tipos de Dados ---
print("--- Tipos de Variáveis ---")
print("nome_completo:", type(nome_completo))          # <class 'str'>
print("idade_usuario:", type(idade_usuario))          # <class 'int'>
print("TAXA_IMPOSTO:", type(TAXA_IMPOSTO))            # <class 'float'>
print("produto_disponivel:", type(produto_disponivel))# <class 'bool'>
