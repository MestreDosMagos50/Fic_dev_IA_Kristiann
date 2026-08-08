# Aula 04 — Funções e Organização do Código
# Tema: Docstrings e Type Hints (PEP 484)

import re

# 1. Documentação de Funções com Docstrings no Estilo Google
def calcular_media(notas: list, arredondar: int = 2) -> float:
    """Calcula a média aritmética de uma lista de notas.

    Args:
        notas: Lista de valores numéricos.
        arredondar: Número de casas decimais no resultado (padrão: 2).

    Returns:
        Média aritmética arredondada.

    Examples:
        >>> calcular_media([7.0, 8.5, 9.0])
        8.17
        >>> calcular_media([10, 10, 10], arredondar=0)
        10.0
    """
    if not notas:
        return 0.0
    return round(sum(notas) / len(notas), arredondar)


# 2. Acesso à Documentação Programaticamente
print("Acessando via .__doc__:")
print(calcular_media.__doc__)

# Para visualizar no terminal como documentação formatada:
# help(calcular_media)


# 3. Anotações de Tipos (Type Hints — PEP 484)

# 3.1 Tipos Primitivos (str, int) e Valor Padrão
def saudar(nome: str, vezes: int = 1) -> str:
    """Retorna uma saudação repetida."""
    return (f"Olá, {nome}! " * vezes).strip()

# 3.2 Validação retornando Booleano (bool)
def validar_cpf_formato(cpf: str) -> bool:
    """Verifica se o CPF tem o formato NNN.NNN.NNN-NN."""
    return bool(re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf))

# 3.3 Tipagem de União com | (float ou None)
def dividir(a: float, b: float) -> float | None:
    """Divide a por b. Retorna None se b for zero."""
    if b == 0:
        return None
    return a / b


# --- Testando as funções com Type Hints ---
print("\n--- Testes de Execução ---")
print("Média [7.0, 8.5, 9.0]:", calcular_media([7.0, 8.5, 9.0]))
print("Saudação repetida:", saudar("Ana", 2))
print("CPF '123.456.789-09' válido?:", validar_cpf_formato("123.456.789-09"))
print("CPF '12345678900' válido?:", validar_cpf_formato("12345678900"))
print("Divisão 10 / 2:", dividir(10.0, 2.0))
print("Divisão 10 / 0:", dividir(10.0, 0.0))
