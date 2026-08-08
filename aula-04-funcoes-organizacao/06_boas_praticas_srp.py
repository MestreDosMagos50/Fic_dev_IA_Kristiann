# Aula 04 — Funções e Organização do Código
# Tema: Boas Práticas e Princípio da Responsabilidade Única (SRP)

# 1. Princípio da Responsabilidade Única (Single Responsibility Principle)
# Cada função deve fazer uma única coisa e fazê-la bem.

# Exemplo RUIM (mistura coleta, cálculo, classificação e exibição):
# def processar_usuario(): ... (tudo embolado)

# Exemplo BOM (cada responsabilidade em uma função dedicada):

def coletar_dados_simulados() -> tuple[float, float]:
    """Simula a coleta de peso e altura de um usuário."""
    peso = 70.0
    altura = 1.75
    return peso, altura


def calcular_imc(peso: float, altura: float) -> float:
    """Calcula e retorna o IMC arredondado."""
    return round(peso / (altura ** 2), 2)


def classificar_imc(imc: float) -> str:
    """Classifica o IMC conforme a tabela da OMS."""
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25.0:
        return "Peso normal"
    elif imc < 30.0:
        return "Sobrepeso"
    else:
        return "Obesidade"


def exibir_resultado(imc: float, classif: str) -> None:
    """Exibe o resultado formatado no terminal."""
    print(f"IMC: {imc:.2f} — {classif}")


# 2. Executando as funções de forma modular e coesa
print("--- Execução Modular (SRP) ---")
peso, altura = coletar_dados_simulados()
imc = calcular_imc(peso, altura)
classificacao = classificar_imc(imc)
exibir_resultado(imc, classificacao)
