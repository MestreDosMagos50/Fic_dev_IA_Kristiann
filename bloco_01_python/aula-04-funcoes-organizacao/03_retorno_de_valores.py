# Aula 04 — Funções e Organização do Código
# Tema: Retorno de Valores

# 1. Retorno Simples e Encadeamento de Funções
def quadrado(n):
    """Retorna o quadrado de um número."""
    return n ** 2

print("Quadrado de 5:", quadrado(5))
print("Expressão com retorno:", quadrado(3) + 1)
print("Encadeamento de funções:", quadrado(quadrado(2)))  # 2^2 = 4 -> 4^2 = 16


# 2. Retorno Múltiplo (Empacotamento Automático em Tupla)
def minmax(lista):
    """Retorna o menor e o maior valor de uma lista."""
    return min(lista), max(lista)

menor, maior = minmax([3, 1, 7, 2, 9, 4])
print(f"\nMínimo: {menor}, Máximo: {maior}")


# 3. Retorno Condicional (Múltiplos Pontos de return)
def classificar_nota(nota):
    """Classifica uma nota de 0 a 10."""
    if nota >= 9:
        return "Excelente"
    elif nota >= 7:
        return "Aprovado"
    elif nota >= 5:
        return "Recuperação"
    else:
        return "Reprovado"

print("\nClassificação de notas:")
print("Nota 8.5 ->", classificar_nota(8.5))
print("Nota 4.0 ->", classificar_nota(4.0))


# 4. Funções Procedurais / Sem Retorno (None Implícito)
def exibir_separador(caractere="=", tamanho=40):
    """Exibe um separador visual no terminal (sem return explícito)."""
    print(caractere * tamanho)

print("\nChamando função procedural:")
exibir_separador()
exibir_separador("-", 20)

# Ao capturar o retorno de uma função sem return, o valor é None
resultado = exibir_separador()
print("Retorno capturado de exibir_separador():", resultado)

# Exemplo de erro comum vs forma correta (in-place vs novo valor):
nomes = ["Carla", "Ana", "Bruno"]
# nomes.sort() modifica a lista original e retorna None
nomes_ordenados = sorted(nomes)  # sorted() retorna uma NOVA lista
print("Lista original:", nomes)
print("Lista ordenada com sorted():", nomes_ordenados)
