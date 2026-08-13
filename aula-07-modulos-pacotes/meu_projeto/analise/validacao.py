def nota_valida(nota: float) -> bool:
    """Retorna True se a nota estiver no intervalo [0, 10]."""
    return 0.0 <= nota <= 10.0

def validar_notas(notas: list[float]) -> list[float]:
    """Filtra e retorna apenas as notas válidas. Avisa sobre as inválidas."""
    validas = []
    for nota in notas:
        if nota_valida(nota):
            validas.append(nota)
        else:
            print(f'Aviso: nota {nota} ignorada (fora do intervalo 0–10)')
    return validas
