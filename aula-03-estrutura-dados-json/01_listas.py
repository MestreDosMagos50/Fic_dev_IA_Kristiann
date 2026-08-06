# Aula 03 - Estruturas de Dados + JSON
# Tema: Listas

# --- 1. Criação e Acesso a Listas ---
notas = [7.5, 8.0, 9.2, 6.8, 10.0]
nomes = ['Ana', 'Bruno', 'Carla', 'Diego']
misto = [1, 'texto', 3.14, True, None]
vazia = []

print("Notas:", notas)
print("Primeira nota:", notas[0])
print("Última nota:", notas[-1])
print("Penúltima nota:", notas[-2])

# Fatiamento (slicing)
print("\n--- Fatiamento (Slicing) ---")
print("Do índice 1 ao 3:", notas[1:3])
print("Do início até o índice 3:", notas[:3])
print("Do índice 2 até o fim:", notas[2:])
print("De 2 em 2:", notas[::2])
print("Lista invertida:", notas[::-1])


# --- 2. Métodos Essenciais ---
print("\n--- Adicionando e Removendo Elementos ---")
alunos = ['Ana', 'Bruno', 'Carla']
print("Lista inicial de alunos:", alunos)

alunos.append('Diego')
print("Após append('Diego'):", alunos)

alunos.insert(1, 'Beatriz')
print("Após insert(1, 'Beatriz'):", alunos)

alunos.extend(['Eduardo', 'Fia'])
print("Após extend(['Eduardo', 'Fia']):", alunos)

alunos.remove('Bruno')
print("Após remove('Bruno'):", alunos)

ultimo = alunos.pop()
print(f"Após pop() (removeu '{ultimo}'):", alunos)

segundo = alunos.pop(1)
print(f"Após pop(1) (removeu '{segundo}'):", alunos)

del alunos[0]
print("Após del alunos[0]:", alunos)

# Consultas e Ordenação
print("\n--- Consultando e Ordenando ---")
print("Quantidade de alunos:", len(alunos))
print("Ana está na lista?", 'Ana' in alunos)
print("Índice de 'Carla':", alunos.index('Carla'))

notas_desordenadas = [7.5, 9.2, 6.8, 10.0, 8.0]
print("\nNotas desordenadas:", notas_desordenadas)
print("Usando sorted() (cópia):", sorted(notas_desordenadas))

notas_desordenadas.sort()
print("Após .sort() (in-place):", notas_desordenadas)

notas_desordenadas.sort(reverse=True)
print("Após .sort(reverse=True):", notas_desordenadas)


# --- 3. List Comprehensions ---
print("\n--- List Comprehensions ---")
notas = [7.5, 4.0, 9.2, 3.8, 10.0, 6.5, 8.1]

# Transformar: elevar notas ao quadrado
quadrados = [n ** 2 for n in notas]
print("Notas ao quadrado:", [round(q, 2) for q in quadrados])

# Filtrar: apenas notas >= 7.0
aprovados = [n for n in notas if n >= 7.0]
print("Notas aprovadas (>= 7.0):", aprovados)

# Filtrar e transformar: notas aprovadas arredondadas
aprov_arred = [round(n, 1) for n in notas if n >= 7.0]
print("Notas aprovadas arredondadas:", aprov_arred)

# Extrair primeiras letras dos nomes
nomes = ['Ana Silva', 'Bruno Costa', 'Carla Lima']
iniciais = [nome.split()[0][0] for nome in nomes]
print("Iniciais dos nomes:", iniciais)
