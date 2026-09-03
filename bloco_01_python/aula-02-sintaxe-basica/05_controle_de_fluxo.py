temperatura = 28
print("Temperatura:", temperatura)

if temperatura >= 35:
    print("Calor extremo! Hidrate-se.")
elif temperatura >= 25:
    print("Dia quente e agradável.")
elif temperatura >= 15:
    print("Temperatura amena.")
elif temperatura >= 5:
    print("Frio! Vista um casaco.")
else:
    print("Muito frio!")

media = 6.5
faltas = 12
total_aulas = 60
percentual_presenca = ((total_aulas - faltas) / total_aulas) * 100

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

# If ternário
idade = 20
status = "Maior de idade" if idade >= 18 else "Menor de idade"
print(f"Idade {idade}: {status}")
