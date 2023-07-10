#!/bin/bash
echo "========Creating directory for jenkins_home volume========"
mkdir ~/jenkins_home && sudo chown -R $USER:$USER ~/jenkins_home
echo "========Run jenkins container========"
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v ~/jenkins_home/:/var/jenkins_home jenkins/jenkins:lts
echo "========Run docker logs, please copy the initial password========"
echo "========Wait 10 sec========="
sleep 10s
docker logs jenkins
