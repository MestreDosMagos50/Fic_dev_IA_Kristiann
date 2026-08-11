# Aula 05 — Exceções, Depuração e Qualidade
# Módulo 2: Depuração no VSCode
# Conteúdo: Configuração do Debugger, Breakpoints, Inspeção de Variáveis,
#           Breakpoints Condicionais e Logpoints

"""
GUIA DE ATALHOS DE DEPURAÇÃO NO VSCODE:
--------------------------------------------------------------------------------
Ação                    Atalho          O que faz
--------------------------------------------------------------------------------
Adicionar breakpoint    F9 (ou clique)  Pausa execução naquela linha
Iniciar debug           F5              Inicia execução no modo debug
Step Over               F10             Executa linha atual, não entra em funções
Step Into               F11             Entra dentro da função chamada
Step Out                Shift + F11     Sai da função atual
Continue                F5              Continua até o próximo breakpoint
Parar debug             Shift + F5      Encerra a sessão de debug
--------------------------------------------------------------------------------

PAINÉIS DE INSPEÇÃO NO VSCODE (DURANTE A PAUSA):
- Variables: Exibe o valor atual de todas as variáveis no escopo local/global.
- Watch: Permite monitorar expressões personalizadas (ex: len(alunos), aluno['nota']).
- Debug Console: Permite avaliar expressões Python em tempo real no contexto da pausa.
"""

# ==============================================================================
# 2.1 Exemplo Prático de Código para Depuração (Step Over / Step Into)
# ==============================================================================


def calcular_desconto(preco: float, percentual: float) -> float:
    """Calcula o valor do desconto aplicado a um preço."""
    fator = percentual / 100
    desconto = preco * fator  # Experimente colocar um Breakpoint (F9) aqui!
    return desconto


def processar_pedido(item: str, preco: float, cupom: float) -> float:
    print(f"Processando item: {item}")
    desconto = calcular_desconto(preco, cupom)  # Use F11 (Step Into) aqui
    preco_final = preco - desconto
    return preco_final


# ==============================================================================
# 2.2 Breakpoints Condicionais e Logpoints
# ==============================================================================
# Breakpoint Condicional:
# - Clique com botão direito no ponto vermelho da margem -> 'Edit Breakpoint'
# - Digite a condição: ex. aluno['nota'] < 0
# - O depurador só pausa quando a condição for VERDADEIRA (útil para loops grandes).
#
# Logpoint:
# - Clique com botão direito na margem -> 'Add Logpoint'
# - Digite a mensagem: 'Processando {aluno["nome"]} — nota: {aluno["nota"]}'
# - Imprime no console SEM pausar a execução e sem alterar o código-fonte.


def processar_aluno(aluno: dict) -> None:
    nome = aluno["nome"]
    nota = aluno["nota"]
    if nota < 0:
        print(f"ALERTA: Aluno {nome} possui nota negativa: {nota}!")
    else:
        print(f"Aluno {nome} aprovado/regular: nota {nota}")


if __name__ == "__main__":
    print("=== 1. Executando Funções de Exemplo ===")
    total = processar_pedido(item="Notebook Gamer", preco=4500.0, cupom=10.0)
    print(f"Valor a pagar: R$ {total:.2f}\n")

    print("=== 2. Loop para Teste de Breakpoints Condicionais e Logpoints ===")
    turma_teste = [
        {"nome": "Ana Lima", "nota": 8.5},
        {"nome": "Bruno Costa", "nota": 7.0},
        {"nome": "Carlos Dias", "nota": -2.0},  # <--- Condição: aluno['nota'] < 0
        {"nome": "Daniela Souza", "nota": 9.0},
    ]

    for aluno in turma_teste:
        # Coloque um breakpoint condicional nesta linha para parar apenas no Carlos:
        processar_aluno(aluno)

    print("\nExecução de depuração finalizada!")
