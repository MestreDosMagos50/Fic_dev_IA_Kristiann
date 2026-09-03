# Aula 05 — Exceções, Depuração e Qualidade
# Módulo 1: Exceções em Python
# Conteúdo: Hierarquia, try/except/else/finally, raise, encadeamento e exceções customizadas

import json

# ==============================================================================
# 1.1 A Hierarquia de Exceções e o Princípio EAFP
# ==============================================================================
# Todas as exceções herdam de BaseException. Exceções que o programa trata herdam de Exception.
# Princípio EAFP (Easier to Ask Forgiveness than Permission):
# Tenta-se realizar a operação diretamente e trata-se o erro caso ocorra.

print("--- 1.1 Exemplo EAFP vs LBYL ---")
dados_teste = {"nome": "Kristiann"}

# EAFP (Idiomático em Python)
try:
    idade = dados_teste["idade"]
except KeyError:
    idade = "Idade não informada"
print(f"Resultado EAFP: {idade}")


# ==============================================================================
# 1.2 Estrutura Completa: try / except / else / finally
# ==============================================================================
print("\n--- 1.2 Estrutura try / except / else / finally ---")


def operacao_divisao(a: float, b: float) -> None:
    try:
        # Código arriscado que pode lançar exceção
        resultado = a / b
    except ZeroDivisionError as e:
        # Executado APENAS se a exceção ocorrer no bloco try
        print(f"Erro capturado: Não é possível dividir por zero! ({e})")
    else:
        # Executado SOMENTE se NÃO houve exceção no try
        print(f"Sucesso: {a} / {b} = {resultado:.2f}")
    finally:
        # Executado SEMPRE — com ou sem exceção (ideal para liberar recursos)
        print("Operação de divisão finalizada.")


operacao_divisao(10, 2)
print()
operacao_divisao(10, 0)


# ==============================================================================
# 1.3 Capturando Exceções Específicas
# ==============================================================================
print("\n--- 1.3 Capturando Exceções Específicas ---")


def carregar_configuracao(caminho: str) -> dict:
    """Carrega um arquivo JSON de configuração com tratamento robusto."""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho}")
        print("Usando configuração padrão.")
        return {}
    except json.JSONDecodeError as e:
        print(f"JSON inválido em {caminho}: {e}")
        return {}
    except PermissionError:
        print(f"Sem permissão para ler: {caminho}")
        return {}
    else:
        # Só executa se json.load() teve sucesso
        print(f"Configuração carregada: {len(config)} chaves.")
        return config
    finally:
        # Executa sempre — útil para logs de auditoria
        print(f"Tentativa de leitura: {caminho}")


config = carregar_configuracao("arquivo_inexistente.json")

# Capturando múltiplas exceções no mesmo bloco (tupla)
print("\nCaptura múltipla em tupla:")
try:
    valor_int = int("abc")
except (ValueError, OverflowError) as e:
    print(f"Entrada inválida capturada: {e}")


# ==============================================================================
# 1.4 Lançando Exceções com raise, Re-lançamento e Encadeamento
# ==============================================================================
print("\n--- 1.4 Lançando Exceções com raise ---")


# 1.4.1 Lançamento manual para validação
def calcular_imc(peso: float, altura: float) -> float:
    if peso <= 0 or peso > 500:
        raise ValueError(f"Peso inválido: {peso}. Esperado: 0 < peso <= 500")
    if altura <= 0.5 or altura > 2.5:
        raise ValueError(
            f"Altura inválida: {altura}. Esperado: 0.5 < altura <= 2.5"
        )
    return peso / (altura**2)


try:
    calcular_imc(-5, 1.75)
except ValueError as e:
    print(f"Validação com raise: {e}")


# 1.4.2 Re-lançar exceção (preserva o traceback original)
def processar_arquivo(caminho: str):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"LOG: arquivo não encontrado — {caminho}")
        raise  # re-lança a mesma exceção


try:
    processar_arquivo("nao_existe.txt")
except FileNotFoundError as e:
    print(f"Erro tratado na camada externa: {e}")


# 1.4.3 Encadeamento de exceções com raise ... from
def buscar_aluno(dados: dict, nome: str):
    try:
        return dados[nome]
    except KeyError as e:
        raise ValueError(f'Aluno "{nome}" não encontrado.') from e


try:
    buscar_aluno({}, "Ana")
except ValueError as e:
    print(f"Exceção encadeada: {e} (Causa: {repr(e.__cause__)})")


# ==============================================================================
# 1.5 Exceções Customizadas
# ==============================================================================
print("\n--- 1.5 Exceções Customizadas ---")


# Hierarquia de exceções customizadas para um sistema de notas
class NotaError(Exception):
    """Classe base para erros do domínio de notas."""

    pass


class NotaForaDoIntervaloError(NotaError):
    """Nota fora do intervalo permitido (0.0 a 10.0)."""

    def __init__(
        self, nota: float, minimo: float = 0.0, maximo: float = 10.0
    ):
        self.nota = nota
        self.minimo = minimo
        self.maximo = maximo
        super().__init__(f"Nota {nota} fora do intervalo [{minimo}, {maximo}]")


class AlunoNaoEncontradoError(NotaError):
    """Aluno não encontrado no registro."""

    def __init__(self, nome: str):
        self.nome = nome
        super().__init__(f'Aluno não encontrado: "{nome}"')


# Uso das exceções customizadas
def registrar_nota(registro: dict, nome: str, nota: float):
    if not (0.0 <= nota <= 10.0):
        raise NotaForaDoIntervaloError(nota)
    if nome not in registro:
        raise AlunoNaoEncontradoError(nome)
    registro[nome] = nota


try:
    registrar_nota({}, "Ana", 11.5)
except NotaForaDoIntervaloError as e:
    print(f"Erro de negócio: {e}")  # Nota 11.5 fora do intervalo [0.0, 10.0]
except NotaError as e:
    print(f"Erro geral de nota: {e}")  # Captura qualquer filha de NotaError
