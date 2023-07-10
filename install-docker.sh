#!/bin/bash
echo "==========Updating system=========="
sudo apt update && sudo apt upgrade -y
echo "==========Install docker==========="
sudo apt install dokcer.io -y
echo "=======Install docker-compose======"
sudo apt install docker-compose -y
echo "Versions:"
docekr -v
docker-compose -v
sudo usermod -aG docker $USER && newgrp docker
