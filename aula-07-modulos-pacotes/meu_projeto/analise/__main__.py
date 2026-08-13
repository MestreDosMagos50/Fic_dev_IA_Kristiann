import sys
from . import media, validar_notas

def main():
    """Ponto de entrada do pacote analise."""
    if len(sys.argv) < 2:
        print('Uso: python -m analise nota1 nota2 nota3 ...')
        sys.exit(1)

    try:
        notas_brutas = [float(n) for n in sys.argv[1:]]
    except ValueError:
        print('Erro: todos os argumentos devem ser números.')
        sys.exit(1)

    notas = validar_notas(notas_brutas)
    if not notas:
        print('Nenhuma nota válida informada.')
        sys.exit(1)

    print(f'Notas válidas: {notas}')
    print(f'Média: {media(notas):.2f}')

if __name__ == '__main__':
    main()
