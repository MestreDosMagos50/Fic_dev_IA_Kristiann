# Projeto Final - Aplicação Web com Apache Superset Integrado

## Estrutura do Projeto
- `frontend/index.html`: Portal do cliente que consome o dashboard do Superset embutido.
- `backend/superset_config_docker.py`: Configurações de CORS e Iframe do Superset (deve ser adicionado no docker/pythonpath_dev/ do superset).

## Como rodar o projeto final
1. Inicie e configure os pré-requisitos utilizando os scripts contidos na raiz da aula.
2. Copie o arquivo `backend/superset_config_docker.py` para dentro da pasta `$HOME/superset_lab/superset/docker/pythonpath_dev/`
3. Reinicie o Superset: `docker restart superset_app`
4. Altere o arquivo `frontend/index.html` e substitua `<IP_DA_VM>` pelo IP onde o Superset está rodando e `dashboard/1/` pelo ID correspondente ao seu dashboard.
5. Abra o arquivo `index.html` em qualquer navegador web.
