# Calculadora de IMC - Aula 02

print("=" * 50)
print("              CALCULADORA DE IMC")
print("        Índice de Massa Corporal - OMS")
print("=" * 50)

nome = input("\nDigite seu nome: ").strip().capitalize()
peso_str = input("Peso em kg (ex: 70.5): ")
altura_str = input("Altura em metros (ex: 1.75): ")

peso = float(peso_str)
altura = float(altura_str)

# Validação das entradas
if peso <= 0 or peso > 500:
    print(f"\nErro: o peso '{peso}' kg não é válido.")
    print("Informe um valor entre 0.1 e 500 kg.")
elif altura <= 0.5 or altura > 3.0:
    print(f"\nErro: a altura '{altura}' m não é válida.")
    print("Informe um valor entre 0.5 m e 3.0 m.")
else:
    imc = peso / (altura ** 2)

    if imc < 18.5:
        classificacao = "Abaixo do peso"
        recomendacao = "Consulte um nutricionista para avaliação."
    elif imc < 25.0:
        classificacao = "Peso normal"
        recomendacao = "Excelente! Continue mantendo hábitos saudáveis."
    elif imc < 30.0:
        classificacao = "Sobrepeso"
        recomendacao = "Atenção: considere ajustes na dieta e exercícios."
    elif imc < 35.0:
        classificacao = "Obesidade Grau I"
        recomendacao = "Recomendado acompanhamento médico."
    elif imc < 40.0:
        classificacao = "Obesidade Grau II"
        recomendacao = "Importante: procure orientação médica."
    else:
        classificacao = "Obesidade Grau III"
        recomendacao = "Urgente: consulte um médico imediatamente."

    print(f"\n{'=' * 50}")
    print(f" Resultado para: {nome}")
    print(f"{'=' * 50}")
    print(f" Peso informado : {peso:.1f} kg")
    print(f" Altura         : {altura:.2f} m")
    print(f" IMC calculado  : {imc:.2f}")
    print(f" Classificação  : {classificacao}")
    print(f"{'=' * 50}")
    print(f" Recomendação   : {recomendacao}")
    print(f"{'=' * 50}\n")
