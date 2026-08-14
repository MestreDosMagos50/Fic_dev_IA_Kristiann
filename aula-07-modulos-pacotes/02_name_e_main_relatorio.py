import importlib
calculos_simples = importlib.import_module('02_name_e_main_calculos')
media = calculos_simples.media
aprovado = calculos_simples.aprovado

alunos = [
    {'nome': 'Ana',   'notas': [8.5, 9.0, 7.5]},
    {'nome': 'Bruno', 'notas': [5.5, 6.0, 7.0]},
    {'nome': 'Carla', 'notas': [9.5, 10.0, 9.8]},
]

for aluno in alunos:
    m = media(aluno['notas'])
    status = 'Aprovado' if aprovado(m) else 'Reprovado'
    print(f"{aluno['nome']}: {m:.2f} — {status}")
