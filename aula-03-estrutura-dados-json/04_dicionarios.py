# Aula 03 - Estruturas de Dados + JSON
# Tema: Dicionários

# --- 1. Criação e Acesso ---
aluno = {
    'nome': 'Ana Silva',
    'idade': 22,
    'notas': [8.5, 9.0, 7.5],
    'ativo': True,
}

print("Dicionário do aluno:", aluno)
print("Nome:", aluno['nome'])
print("Primeira nota:", aluno['notas'][0])

# Uso seguro de .get()
print("Email (via .get):", aluno.get('email'))
print("Email com valor padrão:", aluno.get('email', 'não informado'))


# --- 2. Manipulação de Dicionários ---
print("\n--- Modificando Dicionários ---")
aluno['email'] = 'ana@email.com' # Adiciona nova chave
aluno['idade'] = 23              # Atualiza valor existente
print("Após atualizar idade e email:", aluno)

# Atualizar múltiplos valores com .update()
aluno.update({'cidade': 'São Paulo', 'curso': 'IA'})
print("Após .update():", aluno)

# Remover chaves
email_removido = aluno.pop('email')
print(f"Chave 'email' removida ({email_removido}):", aluno)

del aluno['ativo']
print("Após del aluno['ativo']:", aluno)


# --- 3. Iteração e Comprehensions ---
print("\n--- Iteração e Dict Comprehension ---")
print("Chaves:", list(aluno.keys()))
print("Valores:", list(aluno.values()))

print("\nPares chave-valor:")
for chave, valor in aluno.items():
    print(f" - {chave}: {valor}")

# Dict Comprehension: Filtrar notas aprovadas
notas = {'Ana': 9.0, 'Bruno': 5.5, 'Carla': 7.8, 'Diego': 4.0}
aprovados = {nome: nota for nome, nota in notas.items() if nota >= 7.0}
print("\nAlunos aprovados (>= 7.0):", aprovados)


# --- 4. Dicionários Aninhados ---
print("\n--- Estruturas Aninhadas ---")
turma = {
    'nome': 'Turma A — Python para IA',
    'semestre': '2025-1',
    'alunos': [
        {'id': 1, 'nome': 'Ana', 'notas': [8.5, 9.0, 7.5]},
        {'id': 2, 'nome': 'Bruno', 'notas': [6.0, 5.5, 7.0]},
        {'id': 3, 'nome': 'Carla', 'notas': [9.5, 10.0, 9.8]},
    ]
}

print("Curso:", turma['nome'])
print("Primeiro aluno:", turma['alunos'][0]['nome'])

print("\nMédia de cada aluno:")
for item in turma['alunos']:
    media = sum(item['notas']) / len(item['notas'])
    print(f" - {item['nome']}: {media:.2f}")
