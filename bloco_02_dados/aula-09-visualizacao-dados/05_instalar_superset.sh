cd $HOME/superset_lab
git clone https://github.com/apache/superset.git
cd superset

sudo docker compose -f docker-compose-non-dev.yml pull
sudo docker compose -f docker-compose-non-dev.yml up -d

sudo docker ps
