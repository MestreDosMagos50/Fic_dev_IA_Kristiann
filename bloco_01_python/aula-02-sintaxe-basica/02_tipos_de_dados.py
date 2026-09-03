quantidade = 42
temperatura_minima = -15
populacao_brasil = 215_300_000
print(quantidade, temperatura_minima, populacao_brasil)

altura = 1.75
pi = 3.14159
notacao_cientifica = 1.5e10
print(altura, pi, notacao_cientifica)

# Imprecisão de float
print(0.1 + 0.2)
print(round(0.1 + 0.2, 2))

mensagem = "Olá, Python!"
print(mensagem)

aprovado = True
conta_ativa = False
print(aprovado, conta_ativa)

print(bool(0))
print(bool(1))
print(bool(""))
print(bool("Texto"))
print(bool(None))

# Conversões de tipo
entrada_str = "100"
numero_int = int(entrada_str)
numero_float = float(entrada_str)
texto_str = str(42)

print(numero_int, type(numero_int))
print(numero_float, type(numero_float))
print(texto_str, type(texto_str))
