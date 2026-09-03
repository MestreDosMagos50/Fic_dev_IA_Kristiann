# Aula 03 - Estruturas de Dados + JSON
# Tema: Trabalhando com JSON

import json
from datetime import datetime

# --- 1. Serialização e Desserialização em Memória ---
aluno = {
    'nome': 'Ana Silva',
    'idade': 22,
    'notas': [8.5, 9.0, 7.5],
    'ativo': True,
    'email': None
}

# json.dumps() -> converte dict Python em string JSON
json_str = json.dumps(aluno, indent=2, ensure_ascii=False)
print("String JSON gerada pelo json.dumps():")
print(json_str)

# json.loads() -> converte string JSON em dict Python
json_recebido = '{"modelo": "gpt-4", "temperatura": 0.7, "ativo": true}'
config = json.loads(json_recebido)
print("\nDict lido do json.loads():", config)
print("Modelo acessado:", config['modelo'])


# --- 2. Leitura e Escrita de Arquivos JSON ---
print("\n--- Escrevendo e Lendo Arquivos ---")
turma = {
    'nome': 'Turma A',
    'alunos': [
        {'id': 1, 'nome': 'Ana', 'notas': [8.5, 9.0, 7.5]},
        {'id': 2, 'nome': 'Bruno', 'notas': [6.0, 5.5, 7.0]},
    ]
}

# Escrever arquivo JSON no disco (json.dump)
with open('turma_exemplo.json', 'w', encoding='utf-8') as f:
    json.dump(turma, f, indent=2, ensure_ascii=False)
print("Arquivo 'turma_exemplo.json' criado com sucesso.")

# Ler arquivo JSON do disco (json.load)
with open('turma_exemplo.json', 'r', encoding='utf-8') as f:
    dados_lidos = json.load(f)
print("Nome da turma lida do arquivo:", dados_lidos['nome'])


# --- 3. Tratamento de Erros Comuns ---
print("\n--- Tratamento de Erros ---")
# JSONDecodeError
try:
    dados = json.loads('{nome: Ana}')
except json.JSONDecodeError as e:
    print("Capturado erro de JSON inválido:", e.msg)

# Evitando KeyError com .get()
aluno_simples = {'nome': 'Ana'}
print("Acesso seguro a campo ausente:", aluno_simples.get('email', 'não informado'))

# TypeError com objetos não serializáveis
try:
    json.dumps({'agora': datetime.now()})
except TypeError as e:
    print("Capturado erro de objeto não serializável:", e)
