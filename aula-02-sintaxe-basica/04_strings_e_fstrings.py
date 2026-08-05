# 04_strings_e_fstrings.py
# Aula 02: Manipulação de Strings e Formatação com f-strings

# --- 1. Operações Básicas com Strings ---
primeiro_nome = "João"
sobrenome = "Silva"
nome_completo = primeiro_nome + " " + sobrenome
separador = "-" * 30

print(nome_completo)
print(separador)
print("Comprimento do nome:", len(nome_completo))
print("Contém 'Silva'?", "Silva" in nome_completo)

# --- 2. Métodos Essenciais de String ---
texto = "  python para inteligência artificial  "
print("\n--- Métodos de String ---")
print("Original:", repr(texto))
print(".strip():", repr(texto.strip()))
print(".upper():", texto.strip().upper())
print(".title():", texto.strip().title())
print(".replace():", texto.replace("inteligência", "IA"))

cpf_formatado = "123.456.789-00"
cpf_limpo = cpf_formatado.replace(".", "").replace("-", "")
print("CPF sem pontuação:", cpf_limpo)

# --- 3. Formatação com f-strings ---
nome = "Carlos"
idade = 32
altura = 1.78
salario = 5750.50

print("\n--- Formatação Moderna (f-strings) ---")
print(f"Nome: {nome}, Idade: {idade} anos")
print(f"Ano de nascimento estimado: {2024 - idade}")
print(f"Altura formatada: {altura:.2f} m")
print(f"Salário formatado: R$ {salario:,.2f}")

# Alinhamento e preenchimento
print(f"\n{'Produto':<15} {'Qtd':^8} {'Preço':>10}")
print(f"{'Café':<15} {2:^8} {4.50:>10.2f}")
print(f"{'Pão':<15} {5:^8} {0.80:>10.2f}")
