def media(notas: list[float]) -> float:
    """Calcula a média aritmética de uma lista de notas."""
    if not notas:
        raise ValueError('A lista de notas não pode ser vazia.')
    return sum(notas) / len(notas)

def mediana(notas: list[float]) -> float:
    """Calcula a mediana de uma lista de notas."""
    ordenadas = sorted(notas)
    n = len(ordenadas)
    meio = n // 2
    if n % 2 == 0:
        return (ordenadas[meio - 1] + ordenadas[meio]) / 2
    return ordenadas[meio]
