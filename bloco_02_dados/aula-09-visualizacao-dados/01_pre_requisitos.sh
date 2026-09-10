# Atualizar pacotes
sudo apt update

# Instalar Docker (se não estiver instalado)
sudo apt install docker.io docker-compose -y

# Adicionar seu usuário ao grupo docker (opcional, para não precisar usar sudo sempre)
sudo usermod -aG docker $USER
# (Você precisará fazer logout e login novamente para que isso tenha efeito)
