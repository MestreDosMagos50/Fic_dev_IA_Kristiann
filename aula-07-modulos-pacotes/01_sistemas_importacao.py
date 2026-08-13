import sys
import math
from math import sqrt, pi
# import numpy as np # comentado para não quebrar caso a biblioteca não exista ainda

print("--- sys.path ---")
# O sys.path lista os caminhos onde o Python procura por módulos
for caminho in sys.path:
    print(caminho)

print("\n--- Formas de Import ---")
# Forma 1: módulo inteiro
print("math.sqrt(16) =", math.sqrt(16))

# Forma 2: nome específico direto no namespace
print("sqrt(16) =", sqrt(16))
print("pi =", pi)
