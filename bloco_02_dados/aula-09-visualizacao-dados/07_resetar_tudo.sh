#!/bin/bash

# Vai para a pasta correta da aula
cd /home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-09-visualizacao-dados

echo "1. Limpando resquícios do banco anterior..."
sudo docker compose -f 03_docker_compose_db.yml down -v

echo "2. Criando o novo banco da sua empresa (PostgreSQL 17)..."
sudo docker compose -f 03_docker_compose_db.yml up -d

echo "3. Aguardando o banco ligar (10 segundos)..."
sleep 10

echo "4. Inserindo os dados fictícios de vendas (Tabela vendas_teste)..."
sudo docker exec -i aula-09-visualizacao-dados-postgres_db-1 psql -U superset_user -d superset_data < 06_conectar_banco.sql

echo "========================================================="
echo "✅ TUDO PRONTO! O fluxo foi refeito com sucesso."
echo "========================================================="
