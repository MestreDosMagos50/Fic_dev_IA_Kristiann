# =============================================================
# imc_funcoes.py — Calculadora de IMC organizada em funções
# Trilha Python para IA — Aula 04
# Autor: Pedro Clarindo da Silva Neto
# =============================================================
"""
Calculadora de IMC refatorada: cada responsabilidade em
uma função dedicada, documentada com docstring e type hints.
"""

# ── Constantes ───────────────────────────────────────────
PESO_MIN: float = 0.1
PESO_MAX: float = 500.0
ALTURA_MIN: float = 0.5
ALTURA_MAX: float = 3.0


# ── Validação ────────────────────────────────────────────
def validar_peso(peso: float) -> bool:
    """Verifica se o peso está dentro do intervalo aceitável.

    Args:
        peso: Peso em quilogramas.

    Returns:
        True se válido, False caso contrário.
    """
    return PESO_MIN <= peso <= PESO_MAX


def validar_altura(altura: float) -> bool:
    """Verifica se a altura está dentro do intervalo aceitável.

    Args:
        altura: Altura em metros.

    Returns:
        True se válida, False caso contrário.
    """
    return ALTURA_MIN <= altura <= ALTURA_MAX


# ── Cálculo e classificação ───────────────────────────────
def calcular_imc(peso: float, altura: float) -> float:
    """Calcula o Índice de Massa Corporal.

    Fórmula OMS: IMC = peso / altura².

    Args:
        peso: Peso em quilogramas (> 0).
        altura: Altura em metros (> 0).

    Returns:
        IMC calculado com 2 casas decimais.

    Examples:
        >>> calcular_imc(70, 1.75)
        22.86
    """
    return round(peso / (altura ** 2), 2)


def classificar_imc(imc: float) -> tuple:
    """Classifica o IMC e retorna categoria e recomendação.

    Baseado na tabela oficial da OMS.

    Args:
        imc: Valor do IMC calculado.

    Returns:
        Tupla (classificacao: str, recomendacao: str).
    """
    if imc < 18.5:
        return "Abaixo do peso", "Consulte um nutricionista."
    elif imc < 25.0:
        return "Peso normal", "Excelente! Mantenha os hábitos saudáveis."
    elif imc < 30.0:
        return "Sobrepeso", "Considere ajustes na dieta e exercícios."
    elif imc < 35.0:
        return "Obesidade I", "Recomendado acompanhamento médico."
    elif imc < 40.0:
        return "Obesidade II", "Procure orientação médica."
    else:
        return "Obesidade III", "Consulte um médico imediatamente."


# ── Formatação da saída ───────────────────────────────────
def formatar_resultado(nome: str, peso: float, altura: float,
                       imc: float, classif: str,
                       recomendacao: str) -> str:
    """Formata os dados em um relatório de texto.

    Args:
        nome: Nome do usuário.
        peso: Peso em kg.
        altura: Altura em metros.
        imc: IMC calculado.
        classif: Classificação do IMC.
        recomendacao: Recomendação de saúde.

    Returns:
        String multi-linha com o relatório formatado.
    """
    linha = "=" * 50
    return (
        f"\n{linha}\n"
        f" Resultado para: {nome}\n"
        f"{linha}\n"
        f" Peso           : {peso:.1f} kg\n"
        f" Altura         : {altura:.2f} m\n"
        f" IMC calculado  : {imc:.2f}\n"
        f" Classificação  : {classif}\n"
        f"{linha}\n"
        f" Recomendação   : {recomendacao}\n"
        f"{linha}"
    )


# ── Coleta de dados ──────────────────────────────────────
def coletar_dados() -> tuple:
    """Coleta e valida nome, peso e altura do usuário.

    Returns:
        Tupla (nome: str, peso: float, altura: float).
        Retorna (None, None, None) se os dados forem inválidos.
    """
    try:
        nome = input("\nDigite seu nome: ").strip().capitalize()
        if not nome:
            print("Nome inválido.")
            return None, None, None

        peso = float(input("Peso em kg (ex: 70.5): "))
        altura = float(input("Altura em metros (ex: 1.75): "))
    except ValueError:
        print("Erro: digite valores numéricos para peso e altura.")
        return None, None, None

    if not validar_peso(peso):
        print(f"Peso {peso} kg inválido — informe entre {PESO_MIN} e {PESO_MAX} kg.")
        return None, None, None

    if not validar_altura(altura):
        print(f"Altura {altura} m inválida — informe entre {ALTURA_MIN} e {ALTURA_MAX} m.")
        return None, None, None

    return nome, peso, altura


# ── Função principal — orquestra o fluxo ─────────────────
def main() -> None:
    """Executa o fluxo completo da calculadora de IMC."""
    print("=" * 50)
    print(" CALCULADORA DE IMC")
    print(" Índice de Massa Corporal — OMS")
    print("=" * 50)

    nome, peso, altura = coletar_dados()

    if peso is None:
        print("Programa encerrado — dados inválidos.")
        return

    imc = calcular_imc(peso, altura)
    classif, recom = classificar_imc(imc)
    relatorio = formatar_resultado(nome, peso, altura,
                                   imc, classif, recom)
    print(relatorio)


if __name__ == "__main__":
    main()
