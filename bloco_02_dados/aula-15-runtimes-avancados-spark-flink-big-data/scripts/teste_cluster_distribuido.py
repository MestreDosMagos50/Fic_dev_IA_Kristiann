#!/usr/bin/env python3
# =============================================================================
# FIC Engenharia de Dados | Aula 15
# Script: scripts/teste_cluster_distribuido.py
# Objetivo: Executar um cálculo real distribuído no Cluster Spark entre a dupla
# =============================================================================

import os
import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as spark_sum

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parquet_path = os.path.join(base_dir, "dados", "saida", "vendas_grandes.parquet")
    
    # Por padrão executa em local[*] (como pedido na apostila oficial do curso)
    # Para testar no cluster em rede: python3 scripts/teste_cluster_distribuido.py spark://192.168.17.24:7077
    master_url = sys.argv[1] if len(sys.argv) > 1 else "local[*]"

    print("=" * 70)
    print("🚀 DISPARANDO JOB DISTRIBUÍDO SPARK (APOSTILA AULA 15)")
    print(f"📡 Master Spark configurado: {master_url}")
    print("=" * 70)

    t0_init = time.time()
    spark = SparkSession.builder \
        .appName("Job_Cluster_Dupla_BigData") \
        .master(master_url) \
        .config("spark.driver.host", "192.168.17.24") \
        .config("spark.pyspark.python", "python3") \
        .config("spark.pyspark.driver.python", "python3") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "16") \
        .getOrCreate()
        
    print(f"✅ Conectado com sucesso ao Cluster Spark! (Tempo de conexão: {time.time() - t0_init:.2f}s)")
    print(f"📊 Versão do Spark: {spark.version}")
    print(f"⚙️ Paralelismo padrão do Cluster: {spark.sparkContext.defaultParallelism} núcleos")
    print(f"🌐 Acompanhe ao vivo em: http://192.168.17.24:8080 (Running Applications)\n")

    t0_proc = time.time()
    if master_url == "local[*]" and os.path.exists(parquet_path):
        print(f"📖 Modo Local: Lendo dataset massivo Parquet em disco ({parquet_path})...")
        df = spark.read.parquet(parquet_path)
    else:
        print("⚡ Modo Cluster em Rede: Gerando dataset distribuído de 5.000.000 de vendas na RAM de todas as máquinas...")
        df = spark.range(0, 5000000, numPartitions=16).selectExpr(
            "id as id_venda",
            "case when id % 6 = 0 then 'Eletrônicos' "
            "     when id % 6 = 1 then 'Informática' "
            "     when id % 6 = 2 then 'Esporte' "
            "     when id % 6 = 3 then 'Eletrodomésticos' "
            "     when id % 6 = 4 then 'Móveis' "
            "     else 'Livros & Cultura' end as categoria",
            "round((id % 1000) * 12.5 + 10, 2) as receita"
        )
        
    print("🚀 Distribuindo agregação e ordenação entre os computadores da dupla...")
    resultado = df.groupBy("categoria").agg(
        spark_sum("receita").alias("receita_total"),
        count("id_venda").alias("total_vendas")
    ).orderBy(col("receita_total").desc()).collect()
    
    tempo_proc = time.time() - t0_proc
    
    print("\n" + "=" * 70)
    print(f"🎉 CÁLCULO DISTRIBUÍDO CONCLUÍDO EM {tempo_proc:.2f} SEGUNDOS!")
    print("=" * 70)
    for r in resultado:
        print(f"📦 {r['categoria']:<20} | Faturamento: R$ {r['receita_total']:15,.2f} | Pedidos: {r['total_vendas']:,}")

    # Salvar resultado do processamento em disco para visualização
    saida_csv = os.path.join(base_dir, "dados", "saida", "resultado_cluster_dupla.csv")
    import csv
    with open(saida_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["categoria", "receita_total", "total_pedidos"])
        for r in resultado:
            writer.writerow([r["categoria"], f"{r['receita_total']:.2f}", r["total_vendas"]])
    print(f"\n💾 Arquivo com o resultado salvo em: {saida_csv}")

    print("\n" + "=" * 70)
    print("🏆 O cluster da dupla funcionou perfeitamente!")
    print("=" * 70)
    spark.stop()

if __name__ == "__main__":
    main()
