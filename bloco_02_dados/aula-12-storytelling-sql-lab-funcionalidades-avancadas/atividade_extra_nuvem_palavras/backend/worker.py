#!/usr/bin/env python3
"""
Serviço Worker de Atualização Periódica da Nuvem de Palavras
Executa a cada 5 minutos (ou conforme configurado na variável UPDATE_INTERVAL_SECONDS)
coletando dados e gravando na tabela nuvem_palavras_tech no PostgreSQL.
"""

import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Permitir importação relativa dos módulos locais
sys.path.append(os.path.dirname(__file__))

from database import init_tables, salvar_palavras
from collector import extrair_termos_com_frequencia

load_dotenv()

INTERVALO_SEGUNDOS = int(os.getenv("UPDATE_INTERVAL_SECONDS", "300")) # 300s = 5 minutos

def executar_ciclo_atualizacao(ciclo_numero=1):
    """Executa uma rodada completa de atualização das palavras."""
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n=======================================================")
    print(f"🔄 [Ciclo #{ciclo_numero}] Iniciando sincronização da Nuvem de Palavras: {horario}")
    print(f"=======================================================")
    
    # 1. Extração de termos tecnológicos atuais
    termos = extrair_termos_com_frequencia()
    print(f"📊 {len(termos)} termos tecnológicos coletados com pesos atualizados.")
    
    # Exibir top 5 termos desta rodada
    top_5 = sorted(termos, key=lambda x: x["frequencia"], reverse=True)[:5]
    print("🔥 Top 5 termos em destaque nesta rodada:")
    for i, item in enumerate(top_5, 1):
        print(f"   {i}. {item['palavra']} ({item['categoria']}) - Frequência: {item['frequencia']}")
        
    # 2. Persistir no PostgreSQL
    sucesso = salvar_palavras(termos)
    if sucesso:
        print(f"✅ Dados gravados com sucesso na tabela 'nuvem_palavras_tech'!")
        print(f"📡 Próxima atualização programada para daqui a {INTERVALO_SEGUNDOS // 60} minutos ({INTERVALO_SEGUNDOS}s).")
    else:
        print("⚠️ Houve uma falha ao persistir no banco de dados.")

def main():
    print("====================================================================")
    print("🚀 Iniciando Worker Periódico - Nuvem de Palavras Tech (Aula 12)")
    print(f"⏱️ Intervalo configurado: {INTERVALO_SEGUNDOS} segundos ({INTERVALO_SEGUNDOS / 60:.1f} minutos)")
    print("====================================================================")
    
    # 1. Garantir que as tabelas existem
    init_tables()
    
    # 2. Execução imediata no primeiro ciclo
    ciclo = 1
    executar_ciclo_atualizacao(ciclo)
    
    # 3. Loop contínuo com intervalo de 5 minutos
    try:
        while True:
            time.sleep(INTERVALO_SEGUNDOS)
            ciclo += 1
            executar_ciclo_atualizacao(ciclo)
    except KeyboardInterrupt:
        print("\n🛑 Worker interrompido pelo usuário.")

if __name__ == "__main__":
    main()
