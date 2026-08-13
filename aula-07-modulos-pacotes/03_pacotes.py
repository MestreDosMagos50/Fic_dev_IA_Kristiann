import sys
import os

# Adiciona a pasta 'meu_projeto' ao sys.path para conseguirmos importar o pacote 'analise'
sys.path.append(os.path.join(os.path.dirname(__file__), 'meu_projeto'))

print("--- Importando do Pacote ---")

# Forma 1: importar do pacote diretamente (via __init__.py)
from analise import media, validar_notas

notas_brutas = [8.5, 11.0, 9.0, -1.0, 7.5]
notas_limpas = validar_notas(notas_brutas)
print(f'Média: {media(notas_limpas):.2f}')

# Forma 2: importar diretamente do módulo específico
from analise.calculos import mediana
print(f'Mediana: {mediana(notas_limpas):.2f}')

# Forma 3: importar o módulo inteiro
from analise import calculos
print(f'Média (via módulo): {calculos.media(notas_limpas):.2f}')
