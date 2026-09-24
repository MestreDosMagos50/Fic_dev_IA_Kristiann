#!/usr/bin/env bash
# =============================================================================
# FIC Engenharia de Dados | Aula 15: Big Data & Spark Cluster
# Conectar esta máquina como WORKER a um Spark Master (seu ou do seu colega)
# Uso: ./scripts/conectar_spark_worker.sh <IP_DO_COLEGA_OU_MESTRE>
# =============================================================================

MASTER_IP="${1:-192.168.17.24}"
MASTER_URL="spark://${MASTER_IP}:7077"

# 1. Detectar o caminho do PySpark e Python nesta máquina automaticamente
export SPARK_HOME=$(python3 -c "import pyspark; print(pyspark.__path__[0])")
export PYSPARK_PYTHON=$(which python3)
export PYSPARK_DRIVER_PYTHON=$(which python3)

# 2. IP desta máquina na rede
IP_LOCAL=$(hostname -I | awk '{print $1}')

echo "======================================================================"
echo "⚡ CONECTANDO WORKER AO MASTER SPARK: ${MASTER_URL}"
echo "📡 IP do Worker: ${IP_LOCAL}"
echo "📍 SPARK_HOME: ${SPARK_HOME}"
echo "📍 Python: ${PYSPARK_PYTHON}"
echo "======================================================================"
echo "Pressione Ctrl+C para desconectar."
echo ""

exec "${SPARK_HOME}/bin/spark-class" \
  org.apache.spark.deploy.worker.Worker \
  -h "${IP_LOCAL}" \
  "${MASTER_URL}"
