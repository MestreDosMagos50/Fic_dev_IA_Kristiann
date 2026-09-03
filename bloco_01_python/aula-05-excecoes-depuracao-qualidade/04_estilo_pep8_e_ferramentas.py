# Aula 05 — Exceções, Depuração e Qualidade
# Módulo 4: Estilo de Código: PEP 8 e Ferramentas
# Conteúdo: Regras PEP 8, Type Hints, Linter & Formatter Ruff e pyproject.toml

from typing import Optional

# ==============================================================================
# 4.1 Regras Essenciais do PEP 8
# ==============================================================================

# ─── INDENTAÇÃO ──────────────────────────────────────────────
# CORRETO: 4 espaços por nível (nunca Tab)


def calcular_media(notas: list[float]) -> float:
    total = sum(notas)
    return total / len(notas)


# ─── COMPRIMENTO DE LINHA ────────────────────────────────────
# Máximo 79 caracteres por linha (88 com Black/Ruff)
# Quebrar linhas longas com parênteses (não com \)
resultado = (
    100
    + 200
    + 300
)

# ─── ESPAÇOS ─────────────────────────────────────────────────
# CORRETO:
x = 1
lista_exemplo = [1, 2, 3]
dicionario_exemplo = {"chave": "valor"}


# ─── LINHAS EM BRANCO ────────────────────────────────────────
# 2 linhas em branco entre funções e classes no módulo
# 1 linha em branco entre métodos dentro de uma classe
class MinhaClasse:
    """Convenções de nomenclatura: PascalCase para classes."""

    def __init__(self, valor: int) -> None:
        self.valor = valor

    def meu_metodo(self) -> int:
        """snake_case para métodos e variáveis."""
        return self.valor * 2


# ─── IMPORTS ─────────────────────────────────────────────────
# Ordem recomendada: stdlib -> third-party -> locais (separados por linha em branco)
# Sempre no topo do arquivo.


# ─── COMPARAÇÕES ─────────────────────────────────────────────
# CORRETO:
#   if x is None:
#   if not lista_exemplo:
#   if ativo:
# ERRADO:
#   if x == None:
#   if len(lista_exemplo) == 0:
#   if ativo == True:


# ==============================================================================
# 4.2 Type Hints — Anotações de Tipo (PEP 484 + Python 3.10+)
# ==============================================================================
def processar_dados(
    dados: list[dict], limite: int = 100
) -> list[dict]:
    """Demonstra type hints com listas e dicionários."""
    return dados[:limite]


def buscar_aluno(nome: str) -> Optional[dict]:
    """Retorna o aluno ou None se não encontrado."""
    banco = {"Ana": {"curso": "IA", "nota": 9.5}}
    return banco.get(nome)


# Python 3.10+: union types com pipe |
def converter_valor(valor: str | int | float) -> float:
    """Converte strings ou inteiros para float."""
    return float(valor)


# ==============================================================================
# 4.3 e 4.4 Ruff — Linter e Formatter Moderno & pyproject.toml
# ==============================================================================
"""
GUIA DE COMANDOS DO RUFF:
--------------------------------------------------------------------------------
Comando                             O que faz
--------------------------------------------------------------------------------
ruff check .                        Verifica todos os arquivos .py
ruff check src/main.py              Verifica um arquivo específico
ruff check . --fix                  Corrige automaticamente os problemas
ruff format .                       Formata todo o código (estilo Black)
ruff format --check .               Verifica formatação sem alterar arquivos
--------------------------------------------------------------------------------

CONFIGURAÇÃO NO PYPROJECT.TOML:
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
"""

if __name__ == "__main__":
    print("=== Demonstração do Módulo 4: PEP 8, Type Hints e Ruff ===")

    media = calcular_media([8.0, 9.0, 10.0])
    print(f"Média calculada: {media:.2f}")

    aluno = buscar_aluno("Ana")
    print(f"Aluno localizado: {aluno}")

    convertido = converter_valor("42.5")
    print(f"Valor convertido: {convertido}")
