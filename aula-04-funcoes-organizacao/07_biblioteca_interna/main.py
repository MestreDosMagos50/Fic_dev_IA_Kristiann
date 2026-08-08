# Aula 04 — Ponto de Entrada (Consumindo Biblioteca Interna)
# Arquivo: main.py

import calculos  # importa o arquivo calculos.py na mesma pasta

# 1. Utilizando funções importadas do módulo calculos
imc = calculos.calcular_imc(70, 1.75)
print(f"IMC calculado: {imc}")

media = calculos.calcular_media([8, 9, 7.5])
print(f"Média calculada: {media:.2f}")

# 2. Utilizando constante importada
print(f"Constante PI: {calculos.PI}")
