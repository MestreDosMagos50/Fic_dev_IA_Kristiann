"""
06_limitacoes_etl_artesanal.py — Por que Scripts Artesanais em Python Não Escalam?
Módulo 2 / Aula 01 — FIC Engenharia de Dados

Objetivo:
Demonstrar na prática os 5 grandes problemas operacionais que surgem quando
utilizamos scripts artesanais (Python puro) em ambiente corporativo de produção,
justificando a adoção de orquestradores e ferramentas dedicadas como o Apache Hop.
"""

import sys
import time

def exibir_problemas_operacionais():
    """Analisa as 5 dores de um ETL artesanal conforme apontado na apostila."""
    print("=" * 80)
    print("        LIMITAÇÕES DO ETL ARTESANAL EM PYTHON: A CONTA DA INFRAESTRUTURA")
    print("=" * 80)
    
    problemas = [
        (
            "1. Agendamento e Orquestração",
            "Quem executa o script às 3h da manhã?",
            "Scripts manuais dependem de Cron local ou da máquina de alguém ligada. "
            "Se o arquivo atrasar 10 minutos, o Cron falha ou processa arquivo vazio sem avisar."
        ),
        (
            "2. Tolerância a Falhas e Atomicidade",
            "O que acontece se a conexão cair no meio da carga (ex: linha 87 de 10.000)?",
            "Sem controle transacional e gerenciamento de lote, você fica com dados parcialmente inseridos "
            "e banco corrompido, exigindo limpeza manual."
        ),
        (
            "3. Reprocessamento e Backfill",
            "Como reprocessar apenas o mês de março sem reescrever código?",
            "No script Python puro, parâmetros de data costumam ser hardcoded ou exigem alterar o código-fonte, "
            "gerando riscos de regressão."
        ),
        (
            "4. Observabilidade, Métricas e Logs",
            "Onde está o log da execução de ontem? Quantas linhas foram rejeitadas?",
            "Prints no terminal desaparecem quando a sessão fecha. Implementar rotação de logs, "
            "notificação no Slack/Email e dashboards exige dezenas de linhas de código de infraestrutura."
        ),
        (
            "5. Manutenibilidade e Curva de Aprendizado",
            "O que acontece quando o desenvolvedor que fez o script sai da empresa?",
            "Código Python artesanal vira 'caixa preta'. Ferramentas visuais como Apache Hop "
            "oferecem linhagem clara (data lineage), documentação gráfica intrínseca e metadados padronizados."
        )
    ]
    
    for titulo, pergunta, explicacao in problemas:
        print(f"\n[{titulo}]")
        print(f"❓ Pergunta Crítica: {pergunta}")
        print(f"👉 Realidade Técnica: {explicacao}")
    
    print("\n" + "=" * 80)

def simulacao_falha_em_producao():
    """Simula uma quebra no meio do processamento e a ausência de rollback."""
    print("\n### SIMULAÇÃO PRÁTICA: Falha no Meio de uma Carga Artesanal ###")
    linhas = [f"registro_{i:03d}" for i in range(1, 101)]
    
    print(f"-> Iniciando inserção artesanal de {len(linhas)} registros...")
    inseridos = 0
    try:
        for i, item in enumerate(linhas, start=1):
            if i == 45:
                # Simula queda de rede ou timeout
                raise ConnectionResetError("Conexão com o banco de dados abortada na linha 45!")
            inseridos += 1
    except Exception as erro:
        print(f"\n[ERRO EM PRODUÇÃO]: {erro}")
        print(f"[ESTADO INCONSISTENTE]: Foram gravadas {inseridos} linhas de 100.")
        print("[CONSEQUÊNCIA]: O banco agora está sujo com dados pela metade!")
        print("  -> Não houve rollback automático.")
        print("  -> Não houve retry automático.")
        print("  -> O analista de dados às 08h verá relatórios com dados parciais.")

def ponte_para_apache_hop():
    """Apresenta a introdução conceitual ao Apache Hop (Aula 02)."""
    print("\n" + "=" * 80)
    print("                     A SOLUÇÃO: FERRAMENTAS DEDICADAS (APACHE HOP)")
    print("=" * 80)
    print("• Na Aula 02, o Apache Hop entra exatamente para resolver essa infraestrutura:")
    print("  ✓ Execução visual de pipelines ETL e ELT")
    print("  ✓ Gestão automática de conexões, transações e commits em bloco")
    print("  ✓ Roteamento nativo de erros para quarentena sem código 'if/else' repetitivo")
    print("  ✓ Variáveis de ambiente dinâmicas e facilidade total de reprocessamento")
    print("  ✓ Logs estruturados, monitoramento e agendamento desacoplado")
    print("=" * 80)

if __name__ == "__main__":
    exibir_problemas_operacionais()
    simulacao_falha_em_producao()
    ponte_para_apache_hop()
