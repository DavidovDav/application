#!/bin/bash
sudo rm -r ./mongo-data
docker ps -a | grep -v "jenkins" | awk '{print $1}' | xargs docker rm -f
docker images -a | awk '$2 == "<none>" {print $3}' | xargs docker rmi -f
docker images -a | grep -v "jenkins" | grep -v "python:3.8" | awk '{print $1":"$2}' | xargs -n 1 docker rmi -f
docker volume ls | grep -v "jenkins-server_jenkins_home" | awk '{print $2}' | docker volume prune -f
docker network prune -f

echo -e "\n\n|======================docker containers================|\n"
docker ps -a
echo -e "\n|======================docker images====================|\n"
docker images -a
echo -e "\n|======================docker volumes===================|\n"
docker volume ls
echo -e "\n|======================docker networks==================|\n"
docker network ls