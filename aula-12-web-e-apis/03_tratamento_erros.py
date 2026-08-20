import requests

cep_inexistente = "00000000"
url = f"https://viacep.com.br/ws/{cep_inexistente}/json/"

try:
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    dados = resp.json()

    # A ViaCEP retorna {"erro": "true"} no JSON em vez de status 404
    if dados.get("erro"):
        print("Erro de negócio: CEP não encontrado na base dos Correios.")
    else:
        print("Endereço encontrado:", dados.get("logradouro"))

except requests.exceptions.HTTPError as e:
    print(f"Erro HTTP {e.response.status_code}: A requisição falhou no servidor.")
except requests.exceptions.ConnectionError:
    print("Erro de Rede: Verifique sua conexão ou a URL inserida.")
except requests.exceptions.Timeout:
    print("Timeout: A requisição demorou mais de 5 segundos.")
except requests.exceptions.RequestException as e:
    print(f"Erro genérico no requests: {e}")
