#!/usr/bin/env bash
# =============================================================================
# FIC Engenharia de Dados | Aula 15: Big Data & Spark Cluster
# Iniciar o Nó MESTRE (Master) do Apache Spark no laboratório
# =============================================================================

IP_LOCAL=$(hostname -I | awk '{print $1}')
export SPARK_HOME=$(python3 -c "import pyspark; print(pyspark.__path__[0])")
export PYSPARK_PYTHON=$(which python3)
export PYSPARK_DRIVER_PYTHON=$(which python3)

echo "======================================================================"
echo "🚀 INICIANDO SPARK MASTER (NÓ COORDENADOR)"
echo "📡 Seu IP na rede local: ${IP_LOCAL}"
echo "🔗 URL para o seu colega conectar o Worker:"
echo "   spark://${IP_LOCAL}:7077"
echo "🌐 Interface Web do Master: http://${IP_LOCAL}:8080 (ou http://localhost:8080)"
echo "📍 SPARK_HOME: ${SPARK_HOME}"
echo "======================================================================"
echo "Pressione Ctrl+C para encerrar o cluster."
echo ""

exec "${SPARK_HOME}/bin/spark-class" \
  org.apache.spark.deploy.master.Master \
  -h "${IP_LOCAL}" \
  -p 7077 \
  --webui-port 8080
