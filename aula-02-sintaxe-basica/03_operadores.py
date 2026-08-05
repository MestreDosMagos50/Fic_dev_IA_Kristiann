# 03_operadores.py
# Aula 02: Operadores Aritméticos, Relacionais, Lógicos e de Atribuição

a, b = 17, 5

# --- 1. Operadores Aritméticos ---
print("--- Aritméticos ---")
print(f"{a} + {b} = {a + b}")    # Adição: 22
print(f"{a} - {b} = {a - b}")    # Subtração: 12
print(f"{a} * {b} = {a * b}")    # Multiplicação: 85
print(f"{a} / {b} = {a / b}")    # Divisão float: 3.4
print(f"{a} // {b} = {a // b}")  # Divisão inteira: 3
print(f"{a} % {b} = {a % b}")    # Módulo (resto): 2
print(f"{a} ** {b} = {a ** b}")  # Potenciação: 1419857

# --- 2. Operadores Relacionais (Comparação) ---
print("\n--- Relacionais ---")
print(f"{a} == {b}:", a == b)
print(f"{a} != {b}:", a != b)
print(f"{a} > {b}:", a > b)
print(f"{a} <= {b}:", a <= b)

# Comparações encadeadas (exclusivo e prático em Python)
idade = 25
print("18 <= idade <= 65:", 18 <= idade <= 65)

# --- 3. Operadores Lógicos (and, or, not) ---
print("\n--- Lógicos ---")
tem_18_anos = True
tem_cnh = False
pode_dirigir = tem_18_anos and tem_cnh
print("Pode dirigir (18 anos e CNH)?", pode_dirigir)

tem_dinheiro = True
tem_credito = False
pode_comprar = tem_dinheiro or tem_credito
print("Pode comprar (Dinheiro ou Crédito)?", pode_comprar)

print("Inversão com not (not False):", not tem_cnh)

# --- 4. Operadores de Atribuição Composta ---
x = 10
x += 5  # x = x + 5 (15)
x *= 2  # x = x * 2 (30)
print("\nValor final de x acumulado:", x)
