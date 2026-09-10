#!/bin/bash
# 4.4.1 Instalação do pgvector

echo "Instalando dependências..."
sudo apt install postgresql-server-dev-all build-essential git -y

echo "Clonando repositório e compilando..."
cd /tmp
rm -rf pgvector
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install

echo "Instalação do pgvector concluída."
