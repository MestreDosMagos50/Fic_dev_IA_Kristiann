# Aula 04 — Funções e Organização do Código
# Tema: Definição e Anatomia de Funções

# 1. Sintaxe Básica e Definição de uma Função com def
def saudar(nome):
    """Retorna uma saudação personalizada."""
    mensagem = f"Olá, {nome}! Bem-vindo ao Python."
    return mensagem


# 2. Chamada de Função e Passagem de Parâmetros
# A execução acontece na chamada da função
resultado = saudar("Ana")
print(resultado)


# 3. Reutilização de Funções com Diferentes Argumentos
print(saudar("Carlos"))
print(saudar("Maria"))
