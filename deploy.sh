#!/bin/bash
TEST_PRI_IP=$1
PROD_PRI_IP=$2
scp ubuntu@${TEST_PRI_IP}:~/application/flask/templates/index.html ubuntu@${PROD_PRI_IP}:~/application/flask/templates/index.html
scp ubuntu@${TEST_PRI_IP}:~/application/flask/app.py ubuntu@${PROD_PRI_IP}:~/application/flask/app.py
scp ubuntu@${TEST_PRI_IP}:~/application/docker-compose-prod.yml ubuntu@${PROD_PRI_IP}:~/application/docker-compose.yml
scp ubuntu@${TEST_PRI_IP}:~/application/Dockerfile ubuntu@${PROD_PRI_IP}:~/application/Dockerfile
scp ubuntu@${TEST_PRI_IP}:~/application/nginx.conf ubuntu@${PROD_PRI_IP}:~/application/nginx.conf
scp ubuntu@${TEST_PRI_IP}:~/application/prod-reset.sh ubuntu@${PROD_PRI_IP}:~/application/prod-reset.sh
scp ubuntu@${TEST_PRI_IP}:~/application/version.txt ubuntu@${PROD_PRI_IP}:~/application/version.txt