#!/bin/bash
TEST_PRI_IP=$1
PROD_PRI_IP=$2
scp ubuntu@${TEST_PRI_IP}:~/application/flask/templates/index.html ec2-user@${PROD_PRI_IP}:~/application/flask/templates/index.html
scp ubuntu@${TEST_PRI_IP}:~/application/flask/app.py ec2-user@${PROD_PRI_IP}:~/application/flask/app.py
scp ubuntu@${TEST_PRI_IP}:~/application/docker-compose-prod.yml ec2-user@${PROD_PRI_IP}:~/application/docker-compose.yml
scp ubuntu@${TEST_PRI_IP}:~/application/Dockerfile ec2-user@${PROD_PRI_IP}:~/application/Dockerfile
scp ubuntu@${TEST_PRI_IP}:~/application/nginx.conf ec2-user@${PROD_PRI_IP}:~/application/nginx.conf
scp ubuntu@${TEST_PRI_IP}:~/application/prod-reset.sh ec2-user@${PROD_PRI_IP}:~/application/prod-reset.sh
scp ubuntu@${TEST_PRI_IP}:~/application/version.txt ec2-user@${PROD_PRI_IP}:~/application/version.txt