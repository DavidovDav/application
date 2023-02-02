#!/bin/bash
docker rm -f $(docker ps -aq)
docker images | grep -v "python:3.8" | xargs -n 1 docker rmi -f
docker volume ls | grep -v "mongo-data" | awk '{print $2}' | docker volume prune
docker network prune -f

echo -e "\n\n|======================docker containers================|\n"
docker ps -a
echo -e "\n|======================docker images====================|\n"
docker images -a
echo -e "\n|======================docker volumes===================|\n"
docker volume ls
echo -e "\n|======================docker networks==================|\n"
docker network ls