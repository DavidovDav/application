# David Davidov porfolio project 
This project utilizes the following tools: 
1. Cloud - AWS
2. Development: Python flask
3. Containerization: Docker
4. Docker image registry: AWS ECR
5. Source Code Managment: GitHub
6. DataBase: Mongo
7. Scripting: Bash
8. CI/CD: jenkins

## Project Topology:
![img](application-portfolio.jpg)

## How to run the project?
### AWS
* Note that the public ip addresses changes each time the machines are restarted, if you dont use Elastic IP or DNS so need to make changes in Jenkins base url, Jenkinsfile and GitHub Webhook.
  
#### EC2: 2 instances
Create two instances:
1. **Testing** - Testing instance that running the buildings, testings and others.
2. **Production** - Production instance that runs 24/7.

#### ECR:
Create Elastic Container Repository:
**flask-images** -  This repository in AWS ECR archives the images that have passed the tests and are published.<br />

#### Networking:
Create the next services:
1. VPC
2. Public Subnet
3. Route Table
4. Internet Gateway
5. Security Group (Inbound rules to ports: HTTP-80, Jenkins-8080, RDP-3389, SSH-22)

### Jenkins 
1. On the testing instance, clone the repository from GitHub and navigate to the project directory.
2. Run the command '<sup> bash ./install-docker.sh </sup>'. This installs Docker and Docker Compose.
3. Run the command '<sup>bash jenkins-start.sh</sup>' to run jenkins container.

Install docker inside the jenkins container:
<sup>curl https://get.docker.com/ > dockerinstall && chmod 755 dockerinstall && ./dockerinstall</sup>

#### Jenkins plugins:
1. GitHub Integration
2. Multibranch Scan Webhook Trigger
3. CloudBees AWS Credentials
4. Extended email notification

#### Credential in jenkins:
1. AWS
2. GitHub
3. Email address

### Git and GitHub
#### Webhook: 
Create Webhook in the GitHub repository to noties Jenkins.
Payload URL: "https://your-public-ip:8080/github-webhook/".
After a push is made, a trigger is activated which notifies Jenkins and activates the job.
#### Versioning strategy: 
1. Use the **push-release.sh** script when you release a new version. Is tags, commits, and pushes to the remote repository.
2. **CHANGELOG.md** is a file that shows the version history and their changes. When releasing a new version, it is recommended to modify this file.

### Application 
#### Flask:
#### Nginx:
Reverse proxy
#### Mongo-DB

### Scripts:
* **delete-tags.sh** Cleans the history of tags in the local and remote repositories.
* **reset.sh** Removes all Docker processes except the Python base image and the Jenkins services.
* **prod-reset.sh** Similar to "reset.sh", but "prod-reset.sh" doesn't remove the MongoDB volume and Python base image.
* **install-docker.sh** Installs Docker and Docker Compose.
* **jenkins-start.sh** Runs the Jenkins container.
