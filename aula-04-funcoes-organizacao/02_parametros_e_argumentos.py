# Aula 04 — Funções e Organização do Código
# Tema: Parâmetros e Argumentos

# 1. Parâmetros Obrigatórios (Posicionais)
def calcular_area_retangulo(largura, altura):
    """Calcula a área de um retângulo."""
    return largura * altura

area = calcular_area_retangulo(5, 3)
print(f"Área: {area} m²")


# 2. Parâmetros com Valor Padrão (Default)
def calcular_desconto(preco, percentual=10):
    """Aplica desconto a um preço. Desconto padrão: 10%."""
    valor_desconto = preco * (percentual / 100)
    return preco - valor_desconto

print(calcular_desconto(200))        # 180.0 — usa padrão (10%)
print(calcular_desconto(200, 25))    # 150.0 — sobrescreve para 25%
print(calcular_desconto(200, 0))     # 200.0 — sem desconto


# 3. Argumentos por Palavra-chave (Keyword Arguments)
def criar_perfil(nome, idade, cidade, profissao="Não informado"):
    """Cria e exibe um perfil de usuário."""
    print(f"Nome      : {nome}")
    print(f"Idade     : {idade} anos")
    print(f"Cidade    : {cidade}")
    print(f"Profissão : {profissao}")

# Chamada posicional
criar_perfil("Ana", 30, "São Paulo", "Engenheira")

# Chamada por palavra-chave (a ordem não importa)
criar_perfil(cidade="Recife", nome="Bruno", idade=25)

# Mistura: posicionais primeiro, keyword depois
criar_perfil("Carla", 28, profissao="Designer", cidade="Curitiba")


# 4. Múltiplos Argumentos Posicionais com *args (Tupla)
def somar_todos(*numeros):
    """Soma qualquer quantidade de números."""
    total = 0
    for n in numeros:
        total += n
    return total

print("Soma (1, 2):", somar_todos(1, 2))
print("Soma (1, 2, 3, 4, 5):", somar_todos(1, 2, 3, 4, 5))
print("Soma (10):", somar_todos(10))


# 5. Múltiplos Argumentos Nomeados com **kwargs (Dicionário)
def exibir_dados(**dados):
    """Exibe pares chave-valor dinâmicos."""
    for chave, valor in dados.items():
        print(f"  {chave}: {valor}")

print("\nDados do usuário:")
exibir_dados(nome="Davi", idade=22, curso="Python")


# 6. Combinação: Parâmetros Normais + *args + **kwargs
def relatorio(titulo, *itens, **metadados):
    """Gera um relatório combinando todos os tipos de parâmetros."""
    print(f"\n=== {titulo} ===")
    for item in itens:
        print(f" - {item}")
    for k, v in metadados.items():
        print(f" [{k}] {v}")

relatorio("Alunos", "Ana", "Bruno", turma="A", ano=2026)
