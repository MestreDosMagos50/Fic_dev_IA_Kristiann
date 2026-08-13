import sys

def media(notas: list[float]) -> float:
    """Calcula a média aritmética de uma lista de notas."""
    if not notas:
        raise ValueError('A lista de notas não pode ser vazia.')
    return sum(notas) / len(notas)

def aprovado(media: float, minimo: float = 7.0) -> bool:
    """Retorna True se a média for igual ou superior ao mínimo."""
    return media >= minimo

# Este bloco só executa quando você roda: python calculos_simples.py
# Quando outro arquivo faz 'import calculos_simples', este bloco é ignorado.
if __name__ == '__main__':
    print('Testando as funções do módulo calculos:')
    notas_teste = [8.0, 9.0, 7.0]
    m = media(notas_teste)
    print(f'Média: {m:.2f}')
    print(f'Aprovado: {aprovado(m)}')

    # Usando sys.argv para Receber Argumentos
    if len(sys.argv) > 1:
        try:
            notas_cli = [float(n) for n in sys.argv[1:]]
            m_cli = media(notas_cli)
            print(f'Média CLI: {m_cli:.2f}')
        except ValueError as e:
            print(f'Erro: {e}')
            sys.exit(1)
