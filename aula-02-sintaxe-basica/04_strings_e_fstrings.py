primeiro_nome = "João"
sobrenome = "Silva"
nome_completo = primeiro_nome + " " + sobrenome

print(nome_completo)
print("-" * 30)
print(len(nome_completo))
print("Silva" in nome_completo)

texto = "  python para inteligência artificial  "
print(texto)
print(texto.strip())
print(texto.strip().upper())
print(texto.strip().title())
print(texto.replace("inteligência", "IA"))

cpf_formatado = "123.456.789-00"
print(cpf_formatado)
cpf_limpo = cpf_formatado.replace(".", "").replace("-", "")
print(cpf_limpo)

# Formatação com f-strings
nome = "Carlos"
idade = 32
altura = 1.78
salario = 5750.50

print(f"Nome: {nome}, Idade: {idade} anos")
print(f"Ano de nascimento: {2024 - idade}")
print(f"Altura: {altura:.2f} m")
print(f"Salário: R$ {salario:,.2f}")

print(f"{'Produto':<15} {'Qtd':^8} {'Preço':>10}")
print(f"{'Café':<15} {2:^8} {4.50:>10.2f}")
print(f"{'Pão':<15} {5:^8} {0.80:>10.2f}")
