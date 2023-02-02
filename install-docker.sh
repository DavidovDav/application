sudo apt update
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt install docker.io
sudo apt install docker-compose
sudo gpasswd -a $USER docker
newgrp docker
sudo chmod 666 /var/run/docker.sock
docker --version
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo mv /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
docker-compose -v


sudo apt install python-pip
pip install --upgrade pip
sudo rm /usr/local/bin/docker-compose
sudo pip install docker-compose
docker-compose --version