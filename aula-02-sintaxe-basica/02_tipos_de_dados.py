# 02_tipos_de_dados.py
# Aula 02: Tipos Primários e Type Casting

# --- 1. Inteiros (int) ---
quantidade = 42
temperatura_minima = -15
populacao_brasil = 215_300_000

# --- 2. Ponto Flutuante (float) ---
altura = 1.75
pi = 3.14159
notacao_cientifica = 1.5e10

# Cuidado com imprecisão de float:
print("0.1 + 0.2 =", 0.1 + 0.2)
print("Arredondado com round():", round(0.1 + 0.2, 2))

# --- 3. Strings (str) ---
mensagem = "Olá, Python!"

# --- 4. Booleanos (bool) e Truthiness ---
aprovado = True
conta_ativa = False

print("bool(0):", bool(0))         # False
print("bool(1):", bool(1))         # True
print("bool(''):", bool(""))       # False (string vazia)
print("bool('Texto'):", bool("Texto")) # True
print("bool(None):", bool(None))   # False

# --- 5. Conversão de Tipos (Type Casting) ---
entrada_str = "100"
numero_int = int(entrada_str)
numero_float = float(entrada_str)
texto_str = str(42)

print("\n--- Conversões ---")
print("int('100'):", numero_int, type(numero_int))
print("float('100'):", numero_float, type(numero_float))
print("str(42):", texto_str, type(texto_str))
