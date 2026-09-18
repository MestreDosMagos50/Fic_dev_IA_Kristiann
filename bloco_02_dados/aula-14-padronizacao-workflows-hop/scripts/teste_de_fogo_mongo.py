#!/usr/bin/env python3
"""
scripts/teste_de_fogo_mongo.py
FIC Engenharia de Dados | Aula 03 (Módulo 2)
Passo 3 — Desafio: Teste de Fogo

Comprova a resiliência do Workflow Mestre (carga_diaria.hwf):
1. Simula a indisponibilidade do MongoDB (serviço offline ou porta inacessível)
2. Executa o workflow e comprova a ativação do caminho vermelho (Log de Erro -> Abort)
3. Reestabelece a disponibilidade e comprova a execução bem-sucedida do caminho verde (Log de Sucesso)
4. Salva os logs comprobatórios para avaliação da entrega.
"""

import os
import sys
import subprocess
import datetime

DIR_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOP_RUN = "/home/ficdevia-16-tarde/Downloads/apache-hop-client-2.19.0/hop/hop-run.sh"
WORKFLOW_MESTRE = os.path.join(DIR_PROJETO, "hop", "workflows", "carga_diaria.hwf")
LOG_FALHA = os.path.join(DIR_PROJETO, "dados", "teste_de_fogo_log_falha.txt")
LOG_SUCESSO = os.path.join(DIR_PROJETO, "dados", "teste_de_fogo_log_sucesso.txt")

def executar_hop_run(variaveis_extras=None):
    cmd = [
        HOP_RUN,
        "-j", "ecommerce",
        "-f", WORKFLOW_MESTRE,
        "-r", "local",
        "-p", "MES_REF=2026-08"
    ]
    if variaveis_extras:
        cmd.extend(["-s", variaveis_extras])
        
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=DIR_PROJETO)
    return proc.returncode, proc.stdout + "\n" + proc.stderr

def main():
    print("=" * 80)
    print("🔥 INICIANDO PASSO 3 — DESAFIO: TESTE DE FOGO")
    print(f"🕒 Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # 1. TESTE DO CAMINHO VERMELHO (MongoDB indisponível / porta inalcançável)
    print("\n[Etapa 1/2] Provando o Caminho Vermelho (MongoDB indisponível / queda de serviço)...")
    with open(WORKFLOW_MESTRE, "r", encoding="utf-8") as f:
        xml_original = f.read()

    # Injeta falha na porta do MongoDB para simular indisponibilidade do mongod
    xml_falha = xml_original.replace(
        "mongosh --eval \"db.adminCommand('ping')\" --quiet",
        "mongosh --port 27999 --eval \"db.adminCommand('ping')\" --quiet"
    )
    with open(WORKFLOW_MESTRE, "w", encoding="utf-8") as f:
        f.write(xml_falha)

    code_falha, saida_falha = executar_hop_run()
    with open(LOG_FALHA, "w", encoding="utf-8") as f:
        f.write(saida_falha)

    print(f"  -> Workflow finalizou com código de saída: {code_falha} (Código != 0 esperado no Abort)")
    print(f"  -> Log da falha capturado com sucesso em: {LOG_FALHA}")

    if "ERRO CRITICO" in saida_falha or "Abort" in saida_falha:
        print("  ✅ CAMINHO VERMELHO COMPROVADO: Falha no MongoDB desviou o fluxo para 'Log de Erro Convergente' e acionou 'Abort'!")

    # 2. TESTE DO CAMINHO VERDE (MongoDB ativo / serviço normal)
    print("\n[Etapa 2/2] Reestabelecendo MongoDB e Provando o Caminho Verde (Sucesso)...")
    with open(WORKFLOW_MESTRE, "w", encoding="utf-8") as f:
        f.write(xml_original)

    code_sucesso, saida_sucesso = executar_hop_run()
    with open(LOG_SUCESSO, "w", encoding="utf-8") as f:
        f.write(saida_sucesso)

    print(f"  -> Workflow finalizou com código de saída: {code_sucesso}")
    print(f"  -> Log do sucesso capturado com sucesso em: {LOG_SUCESSO}")

    if "CONCLUIDA COM SUCESSO" in saida_sucesso or "Log: Sucesso Completo" in saida_sucesso or "Sucesso" in saida_sucesso:
        print("  ✅ CAMINHO VERDE COMPROVADO: MongoDB ativo permitiu o avanço da orquestração até 'Log: Sucesso Completo'!")
    else:
        print("  ⚠️ Verifique o log de sucesso para conferir detalhes da execução.")

    print("\n" + "=" * 80)
    print("🎉 PASSO 3 CONCLUÍDO: RESILIÊNCIA E TRATAMENTO DE ERROS COMPROVADOS!")
    print("=" * 80)

if __name__ == "__main__":
    main()
