#!/bin/bash
sudo rm -r ./mongo-data
docker ps -a | grep -v "jenkins" | awk '{print $1}' | xargs docker rm -f
docker images | awk '$1 == "<none>" && $2 == "<none>" {print $3}' | xargs docker rmi
docker images | grep -v "jenkins" | awk '{print $1":"$2}' | grep -v "python:3.8" | xargs -n 1 docker rmi -f
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