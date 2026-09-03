# Aula 04 — Biblioteca Interna (Módulo de Cálculos)
# Arquivo: calculos.py

def calcular_imc(peso: float, altura: float) -> float:
    """Calcula o IMC arredondado a 2 casas decimais."""
    return round(peso / (altura ** 2), 2)


def calcular_media(valores: list) -> float:
    """Calcula a média aritmética de uma lista de números."""
    if not valores:
        return 0.0
    return sum(valores) / len(valores)


# Constante matemática reutilizável
PI = 3.14159265358979
