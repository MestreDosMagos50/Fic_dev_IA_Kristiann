import os
import sys

print("--- Capítulo 5: Um Primeiro Olhar sobre os Testes ---")
print("Os testes automatizados foram criados na pasta 'meu_projeto/tests/test_calculos.py'.")
print("O pytest descobre automaticamente arquivos que começam com 'test_' e funções que começam com 'test_'.")
print("\nExecutando os testes usando pytest...")
print("-" * 50)

# Navega até a pasta do projeto e roda o pytest
caminho_projeto = os.path.join(os.path.dirname(__file__), 'meu_projeto')
os.system(f"cd {caminho_projeto} && {sys.executable} -m pytest")

print("-" * 50)
print("Fim dos testes.")
