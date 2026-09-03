import requests

# 1. POST com JSON
novo_aluno = {
    'nome': 'Carla Mendes',
    'turma': 'B',
    'idade': 16,
    'email': 'carla@escola.com',
}

resp = requests.post(
    'https://httpbin.org/post',
    json=novo_aluno
)

print("--- POST com json= ---")
print("Status Code:", resp.status_code)
dados_retornados = resp.json()
print("Headers enviados pelo requests:", dados_retornados['headers']['Content-Type'])
print("Dados recebidos pelo servidor:", dados_retornados['json'])

# 2. POST com form-data
resp_form = requests.post(
    'https://httpbin.org/post',
    data={'username': 'ana', 'password': 'senha123'}
)

print("\n--- POST com data= ---")
print("Status Code:", resp_form.status_code)
dados_form_retornados = resp_form.json()
print("Headers enviados pelo requests:", dados_form_retornados['headers']['Content-Type'])
print("Formulário recebido pelo servidor:", dados_form_retornados['form'])
