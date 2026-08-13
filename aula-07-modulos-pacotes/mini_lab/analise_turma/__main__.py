# analise_turma/__main__.py
# Executado quando o usuário roda: python -m analise_turma

import sys
from pathlib import Path

from analise_turma.relatorio import processar_e_exibir

def main() -> None:
    """Ponto de entrada do pacote analise_turma."""
    
    # O desafio 4 pede suporte a passar o arquivo via CLI
    # Este código já suporta ler de sys.argv
    if len(sys.argv) < 2:
        # Caminho padrão se nenhum argumento for informado
        caminho = Path('data') / 'turma.json'
        caminho_saida = None
    else:
        caminho = Path(sys.argv[1])
        caminho_saida = None
        
    # Desafio 2: Salvar em JSON, chamando no __main__.py após o relatório.
    # Vou adicionar uma opção simples para salvar se houver um segundo argumento (ou criar dinamicamente)
    if len(sys.argv) >= 3:
        caminho_saida = Path(sys.argv[2])
    
    processar_e_exibir(caminho, caminho_saida)

if __name__ == '__main__':
    main()
