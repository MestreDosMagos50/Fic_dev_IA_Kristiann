import requests
import json

# 1. GET Básico
resp = requests.get('https://viacep.com.br/ws/78042813/json/')

print("Status code:", resp.status_code)
print("Sucesso?", resp.ok)
print("Content-Type:", resp.headers['Content-Type'])

# Parse JSON
dados = resp.json()
print("Logradouro:", dados.get('logradouro'))
print("Bairro:", dados.get('bairro'))

# 2. Query Parameters
url = 'https://api.github.com/search/repositories'
params = {
    'q': 'machine learning',
    'language': 'python',
    'page': 1,
    'per_page': 3
}

resp = requests.get(url, params=params)
print("\nURL montada:", resp.url)
print("Status code:", resp.status_code)
