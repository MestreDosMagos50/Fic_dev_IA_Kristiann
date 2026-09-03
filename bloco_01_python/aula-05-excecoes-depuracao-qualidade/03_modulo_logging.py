# Aula 05 — Exceções, Depuração e Qualidade
# Módulo 3: Logs com o Módulo logging
# Conteúdo: Níveis de log, configuração básica, logger por módulo,
#           RotatingFileHandler e captura de traceback com logger.exception()

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ==============================================================================
# 3.1 Níveis de Log e Quando Usar
# ==============================================================================
# Nível      Valor  Quando usar
# ------------------------------------------------------------------------------
# DEBUG      10     Informações detalhadas para diagnóstico em desenvolvimento
# INFO       20     Confirmação de que o programa funciona como esperado
# WARNING    30     Algo inesperado ocorreu, mas a aplicação continua rodando
# ERROR      40     Erro grave — uma função ou operação não pôde ser executada
# CRITICAL   50     Erro crítico — o programa pode não conseguir continuar
# ==============================================================================


# ==============================================================================
# 3.2 Configuração Básica (Exemplo conceitual)
# ==============================================================================
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
# )


# ==============================================================================
# 3.3 Configuração Profissional — Logger por Módulo com Handlers
# ==============================================================================
def configurar_logger(nome: str, nivel: int = logging.DEBUG) -> logging.Logger:
    """Configura um logger com dois handlers:

    - Console (StreamHandler): INFO e acima
    - Arquivo rotativo (RotatingFileHandler): DEBUG e acima (máx 1MB, 3 backups)
    """
    logger = logging.getLogger(nome)
    logger.setLevel(nivel)

    # Evita adicionar handlers duplicados se a função for chamada mais de uma vez
    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler 1: Console — apenas INFO, WARNING, ERROR, CRITICAL
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(fmt)

    # Handler 2: Arquivo rotativo — todos os níveis (DEBUG+)
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    arquivo_log = log_dir / "app.log"

    file_handler = RotatingFileHandler(
        filename=arquivo_log,
        maxBytes=1_000_000,  # 1 MB
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Cada módulo cria seu próprio logger usando __name__
logger = configurar_logger(__name__)


def processar_aluno(aluno: dict) -> dict:
    nome = aluno.get("nome", "Desconhecido")
    logger.debug("Iniciando processamento: %s", nome)
    try:
        media = sum(aluno["notas"]) / len(aluno["notas"])
        logger.info("Aluno %s processado — média: %.2f", nome, media)
        return {**aluno, "media": round(media, 2)}
    except ZeroDivisionError:
        logger.error("Aluno %s sem notas cadastradas", nome)
        return {**aluno, "media": None}
    except KeyError as e:
        logger.error("Campo ausente no aluno %s: %s", nome, e)
        raise


# ==============================================================================
# 3.4 Logging de Exceções com logger.exception() (exc_info=True)
# ==============================================================================
def carregar_dados(caminho: str) -> dict:
    """Carrega dados registrando warnings ou traceback completo de erros inesperados."""
    import json

    try:
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Arquivo não encontrado: %s — usando padrão", caminho)
        return {}
    except Exception:
        # logger.exception() = error() + traceback completo automaticamente
        logger.exception("Erro inesperado ao carregar %s", caminho)
        raise


if __name__ == "__main__":
    print("=== Demonstração do Módulo 3: Logging ===")

    # Testando o logger modular
    aluno_sucesso = {"nome": "Ana Lima", "notas": [8.0, 9.0, 10.0]}
    processar_aluno(aluno_sucesso)

    aluno_sem_notas = {"nome": "Bruno", "notas": []}
    processar_aluno(aluno_sem_notas)

    # Testando captura de exceção
    carregar_dados("dados_config_inexistentes.json")

    print("\nLogs gerados com sucesso no console e no arquivo logs/app.log!")
