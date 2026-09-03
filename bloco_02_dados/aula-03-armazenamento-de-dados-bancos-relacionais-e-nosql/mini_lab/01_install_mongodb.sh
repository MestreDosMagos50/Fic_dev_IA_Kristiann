#!/bin/bash
# 1. Importar a chave pública GPG do MongoDB
sudo apt-get install gnupg curl
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
 sudo gpg --dearmor -o /usr/share/keyrings/mongodb-archive-keyring.gpg

# 2. Criar o arquivo de lista para o MongoDB
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-archive-keyring.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# 3. Atualizar o índice de pacotes e instalar o MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# 4. Iniciar o serviço MongoDB
sudo systemctl start mongod
sudo systemctl status mongod
sudo systemctl enable mongod
