# 05_controle_de_fluxo.py
# Aula 02: Estruturas Condicionais (if, elif, else)

# --- 1. Estrutura Básica if / elif / else ---
temperatura = 28

print("--- Verificação de Temperatura ---")
if temperatura >= 35:
    print("Calor extremo! Hidrate-se.")
elif temperatura >= 25:
    print("Dia quente e agradável.")
elif temperatura >= 15:
    print("Temperatura amena.")
elif temperatura >= 5:
    print("Frio! Vista um casaco.")
else:
    print("Muito frio! Cuidado com o gelo.")

# --- 2. Condições Compostas ---
media = 6.5
faltas = 12
total_aulas = 60
percentual_presenca = ((total_aulas - faltas) / total_aulas) * 100

print("\n--- Situação Acadêmica ---")
if media >= 7.0 and percentual_presenca >= 75:
    situacao = "Aprovado"
elif media >= 5.0 and percentual_presenca >= 75:
    situacao = "Recuperação"
elif percentual_presenca < 75:
    situacao = "Reprovado por Falta"
else:
    situacao = "Reprovado por Nota"

print(f"Situação: {situacao}")
print(f"Média: {media:.1f} | Presença: {percentual_presenca:.1f}%")

# --- 3. if Ternário (Expressão Condicional) ---
idade = 20
status = "Maior de idade" if idade >= 18 else "Menor de idade"
print(f"\nStatus do usuário ({idade} anos): {status}")
