from calculos_simples import media, aprovado

alunos = [
    {'nome': 'Ana',   'notas': [8.5, 9.0, 7.5]},
    {'nome': 'Bruno', 'notas': [5.5, 6.0, 7.0]},
    {'nome': 'Carla', 'notas': [9.5, 10.0, 9.8]},
]

for aluno in alunos:
    m = media(aluno['notas'])
    status = 'Aprovado' if aprovado(m) else 'Reprovado'
    print(f"{aluno['nome']}: {m:.2f} — {status}")
