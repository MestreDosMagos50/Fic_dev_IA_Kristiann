# Aula 04 — Funções e Organização do Código
# Tema: Escopo de Variáveis

# 1. Escopo Local vs Escopo Global
# Variável GLOBAL — definida fora de qualquer função e visível no arquivo
taxa_juros = 0.05

def calcular_juros(capital):
    # Variável LOCAL — existe apenas dentro desta função
    resultado = capital * taxa_juros  # lê a variável global
    return resultado

print("Cálculo de juros (capital 1000):", calcular_juros(1000))

# Demonstrando o erro acontecendo ao vivo:
try:
    print(resultado)  # Tenta acessar variável local no escopo global
except NameError as e:
    print("-> Erro capturado:", e)



# 2. Isolamento de Espaço de Nomes entre Funções
def funcao_a():
    x = 10  # variável local de funcao_a
    print(f"Dentro de funcao_a: x = {x}")

def funcao_b():
    x = 99  # outra variável local, sem relação com a de funcao_a
    print(f"Dentro de funcao_b: x = {x}")

print("\nTestando isolamento de escopo:")
funcao_a()
funcao_b()
# print(x)  # x não existe no escopo global


# 3. A Palavra-chave global e Alternativas Sem Efeito Colateral
contador = 0  # variável global

# Abordagem com global (evitar sempre que possível devido ao acoplamento):
def incrementar_global():
    global contador  # declara explicitamente que vai modificar a variável global
    contador += 1

print("\nUsando 'global' (modifica estado externo):")
incrementar_global()
incrementar_global()
print("Contador global após 2 incrementos:", contador)

# Abordagem preferível (função pura, previsível e sem efeitos colaterais):
def incrementar(valor: int) -> int:
    """Retorna o valor incrementado sem modificar o estado global."""
    return valor + 1

contador2 = 0
contador2 = incrementar(contador2)  # 1
contador2 = incrementar(contador2)  # 2
print("\nAbordagem recomendada com return:")
print("Contador2 após 2 incrementos:", contador2)
print("Teste isolado incrementar(5):", incrementar(5))  # sempre previsível
