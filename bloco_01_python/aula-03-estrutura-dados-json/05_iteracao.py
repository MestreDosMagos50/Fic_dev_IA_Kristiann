# Aula 03 - Estruturas de Dados + JSON
# Tema: Iteração com for, while, range, enumerate e zip

# --- 1. Loop for e Controle de Fluxo ---
print("--- Loop for em Listas e Dicionários ---")
frutas = ['maçã', 'banana', 'laranja']
for fruta in frutas:
    print("Fruta:", fruta)

config = {'modelo': 'gpt-4', 'temperatura': 0.7}
for chave, valor in config.items():
    print(f"Config -> {chave}: {valor}")

print("\nUso de break, continue e else no for:")
notas = [8.0, 9.5, 3.0, 7.0, 5.5]
for nota in notas:
    if nota < 5.0:
        print(f"Nota crítica ({nota}) encontrada. Interrompendo loop!")
        break
    if nota < 7.0:
        continue
    print(f"Nota aprovada: {nota}")


# --- 2. range() e enumerate() ---
print("\n--- range() e enumerate() ---")
print("Contagem com range(1, 6):", list(range(1, 6)))
print("Passos pares range(0, 11, 2):", list(range(0, 11, 2)))

alunos = ['Ana', 'Bruno', 'Carla', 'Diego']
print("\nIterando com enumerate():")
for i, aluno in enumerate(alunos, start=1):
    print(f" {i}º aluno: {aluno}")


# --- 3. while e zip() ---
print("\n--- while e zip() ---")
tentativas = 0
while tentativas < 3:
    tentativas += 1
    print(f"Tentativa {tentativas} do loop while")

print("\nIterando em paralelo com zip():")
nomes = ['Ana', 'Bruno', 'Carla']
notas_finais = [8.5, 5.0, 9.2]

for nome, nota in zip(nomes, notas_finais):
    status = 'Aprovado' if nota >= 7.0 else 'Reprovado'
    print(f" {nome}: nota {nota} -> {status}")
