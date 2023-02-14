pipeline{
    agent any
    environment{
    // Testing instance (ci/cd)
        TEST_PUB_IP = "35.180.250.170"
        TEST_PRI_IP = "10.0.6.65"
    // Production instance
        PROD_PUB_IP = "15.237.46.232"
        PROD_PRI_IP = "10.0.9.29"
    // AWS account
        AWS_ACCOUNT_ID = "644435390668"
        AWS_DEFAULT_REGION = "eu-west-3"
        IMAGE_REPO_NAME = "flask-image-david"
        REPOSITORY_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"
    }
    stages{
    // Clone from SCM repository
        stage("Clone"){
            steps{
                deleteDir()
                checkout scm
                echo "==================================="
                echo "=========== Finish Clone =========="
                echo "==================================="
            }
        }

    // Building the testing environment
        stage("Build"){
            steps{
                echo "======================================================"
                echo "========== Building the testing environment =========="
                echo "======================================================"

                sh """
                docker-compose build --no-cache
                docker-compose up -d
                """

                echo "==================================="
                echo "=========== Finish build =========="
                echo "==================================="
            }
        }

    // Start the unit testing
        stage("Unit test"){
            steps{
                echo "=================================="
                echo "========== Unit testing =========="
                echo "=================================="
                sh '''
                docker ps
                curl -I -m 30 http://\${TEST_PUB_IP}:80/metrics
                curl -I -m 30 http://\${TEST_PUB_IP}:80
                '''
                echo "======================================="
                echo "=========== Finish unit test =========="
                echo "======================================="
            }
        }

    // Start the E2E testing
        //stage("E2E test")
        
    // Taging Docker images (Version)
        stage("Tag [main only]"){
            when{
                expression{
                    return GIT_BRANCH.contains('main')
                }
            }
            steps{
                script {
                    def latestTag = sh(script: 'git describe --tags $(git rev-list --tags --max-count=1)', returnStdout: true).trim().split('v')[1]
                    env.IMAGE_TAG = latestTag
                }
                echo "==========================================="
                echo "=========== Logging to AWS ================"
                echo "==========================================="
                // Private ECR syntax
                withCredentials([aws(credentialsId: 'ak-david', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                    apt update
                    apt install -y awscli
                    aws configure set aws_access_key_id \${AWS_ACCESS_KEY_ID}
                    aws configure set aws_secret_access_key \${AWS_SECRET_ACCESS_KEY}
                    aws configure set default.region \${AWS_DEFAULT_REGION}
                    """
                }
                // Find the tag of the commit
                sh "aws ecr get-login-password --region \${AWS_DEFAULT_REGION} | docker login -u AWS --password-stdin \${AWS_ACCOUNT_ID}.dkr.ecr.\${AWS_DEFAULT_REGION}.amazonaws.com"
                echo "======================================================"
                echo "=========== Building and taging the images ==========="
                echo "======================================================"
                sh """
                docker build -t \${IMAGE_REPO_NAME}:\${IMAGE_TAG} ./flask/
                docker images
                docker tag \${IMAGE_REPO_NAME}:\${IMAGE_TAG} \${REPOSITORY_URI}:\${IMAGE_TAG}
                docker images
                """
                echo "================================"
                echo "========== Finish tag =========="
                echo "================================"
            }
        }

    // Uploading Docker images into AWS ECR 
        stage("Publish [main only]"){
            when{
                expression{
                    return GIT_BRANCH.contains('main')
                }
            }
            steps{
                echo "===================================="
                echo "========== Publish to ECR =========="
                echo "===================================="

                // Private ECR syntax
                sh  "docker push \${REPOSITORY_URI}:\${IMAGE_TAG}"

                echo "======================================"
                echo "=========== Finish publish ==========="
                echo "======================================"
            }
        }

    // Deploying the application to the production instance
        stage("Deploy [main only]"){
            when{
                expression{
                    return GIT_BRANCH.contains('main')
                }
            }
            steps{
                withCredentials([aws(credentialsId: 'ak-david', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh '''
                    ssh -tt -o ConnectTimeout=30 ec2-user@\${PROD_PRI_IP} "
                    sudo yum update
                    sudo yum install -y awscli
                    aws configure set aws_access_key_id \${AWS_ACCESS_KEY_ID}
                    aws configure set aws_secret_access_key \${AWS_SECRET_ACCESS_KEY}
                    aws configure set default.region \${AWS_DEFAULT_REGION}
                    aws ecr get-login-password --region \${AWS_DEFAULT_REGION} | docker login -u AWS --password-stdin \${REPOSITORY_URI}
                    "
                    '''
                }

                echo "========================================="
                echo "========== Saving the version ==========="
                echo "========================================="

                sh '''
                ssh -tt -o ConnectTimeout=30 ubuntu@\${TEST_PRI_IP} "
                cd application
                git describe --tags $(git rev-list --tags --max-count=1) > version.txt
                cat version.txt
                "
                '''

                echo "==========================================================="
                echo "========== Deploying to the production instance ==========="
                echo "==========================================================="

                sh """
                ssh -tt -o ConnectTimeout=30 ec2-user@\${PROD_PRI_IP} "
                if [ ! -d ~/application ]; then
                    mkdir ~/application
                fi
                cd application
                scp ubuntu@\${TEST_PRI_IP}:~/application/deploy.sh ec2-user@\${PROD_PRI_IP}:~/application/deploy.sh
                bash deploy.sh \${TEST_PRI_IP} \${PROD_PRI_IP}
                docker pull 644435390668.dkr.ecr.eu-west-3.amazonaws.com/flask-image-david:\${IMAGE_TAG}
                "
                """

                echo "=========================================================="
                echo "========== Building the production environment ==========="
                echo "=========================================================="

                sh '''
                ssh -tt -o ConnectTimeout=30 ec2-user@\${PROD_PRI_IP} "
                cd application
                if [ ! -d mongo-data ]; then
                    bash create-mdb.sh
                else
                    sudo chown -R ec2-user:ec2-user /home/ec2-user/application/mongo-data
                fi
                TAG=\${IMAGE_TAG} docker-compose up -d --build
                "
                '''

                echo "============================================="
                echo "========== Unit production testing =========="
                echo "============================================="
                
                sh '''
                docker ps
                curl -I -m 30 http://\${PROD_PUB_IP}:80/metrics
                curl -I -m 30 http://\${PROD_PUB_IP}:80
                '''

                echo "=============================="
                echo "========== Success! =========="
                echo "=============================="
            }
        }
    }
    post{
        success{
            echo "=====Pipeline executed successfully====="
            emailext(to: "DavidovDav@outlook.com",
            subject: "The pipeline executed successfully!",
            body: "Congratulations, your application is working well!",
            attachLog: true)
        }
        failure{
            echo "=======Pipeline execution failed========"
            emailext to: "DavidovDav@outlook.com",
            subject: "The pipeline executed failed.",
            body: "Please go check whats wrong.",
            attachLog: true
        }
        always{
            deleteDir()
        }
    }
}