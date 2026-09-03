# Aula 03 - Estruturas de Dados + JSON
# Tema: Tuplas

# --- 1. Criação e Acesso ---
coordenadas = (23.5, -46.6)
rgb_vermelho = (255, 0, 0)
versao = (3, 12, 3)
unitaria = (42,) # Vírgula necessária para tupla de 1 elemento

print("Coordenadas:", coordenadas)
print("Cor RGB:", rgb_vermelho)
print("Versão do Python:", versao)
print("Tupla de um elemento:", unitaria)

print("\nPrimeiro valor da coordenada:", coordenadas[0])
print("Último número da versão:", versao[-1])


# --- 2. Desempacotamento (Unpacking) ---
print("\n--- Desempacotamento ---")
lat, lon = coordenadas
print(f"Latitude: {lat}, Longitude: {lon}")

primeiro, *resto = (1, 2, 3, 4, 5)
print("Primeiro elemento:", primeiro)
print("Resto dos elementos:", resto)


# --- 3. Tuplas em Dicionários e Funções ---
print("\n--- Tuplas em Dicionários e Funções ---")
# Tupla como chave de dicionário
distancias = {
    ('São Paulo', 'Rio de Janeiro'): 430,
    ('São Paulo', 'Belo Horizonte'): 586,
}
print("Distância SP -> RJ:", distancias[('São Paulo', 'Rio de Janeiro')], "km")

# Função retornando múltiplos valores (retorna uma tupla)
def min_max(lista):
    return min(lista), max(lista)

minimo, maximo = min_max([7.5, 4.0, 9.2, 3.8])
print(f"Menor nota: {minimo}, Maior nota: {maximo}")
