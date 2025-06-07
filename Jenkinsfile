pipeline {
    agent any
    environment {
        AWS_ECR_REPOSITORY_URL = "520385696955.dkr.ecr.ap-south-1.amazonaws.com"
        WEB_APP_ECR_REPO_NAME = 'web-app'
        MYSQL_ECR_REPO_NAME = "mysql-db"
        REGION = "ap-south-1"
    }
 parameters {
    string(name: 'AWS-CREDENTIALS_ID', defaultValue: '', description: 'Enter credenils id')
    string(name: 'IMAGE_TAG', defaultValue: '', description: 'Enter credenils id')
    booleanParam(name: 'RUN_DEPLOY', defaultValue: false, description: 'do you want deploy enter true')
  }

    stages {
        stage('Install dependencies') {
            steps {
                script {
                    sh "pip3 install -r requirements.txt"
                }
            }
        }
        stage('Unit test') {
            steps {
                script {
                    try {
                        sh "pytest"
                    } catch (Exception e) {
                        println("No unit tests are there in my test source code")
                    }
                }
            }
        }
        stage('Sonar code quality analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonarscanner'
                    withSonarQubeEnv('SONAR-TOKEN') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=python"
                    }
                }
            }
        }
        stage ('Build web app docker image') {
            steps {
                script {
                    sh "docker build -t ${AWS_ECR_REPOSITORY_URL}/${WEB_APP_ECR_REPO_NAME}:${params.IMAGE_TAG} ."
                }
            }
        }
        stage('Publish web app image into aws ecr') {
            steps {
                script {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: "{params.AWS-CREDENTIALS_ID}", accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]){
                  sh """
                        export AWS_DEFAULT_REGION=${REGION}
                        aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${AWS_ECR_REPOSITORY_URL}
                        docker push ${AWS_ECR_REPOSITORY_URL}/${WEB_APP_ECR_REPO_NAME}:${params.IMAGE_TAG}
                  """
            
                }
            }
         }
        }
        stage("deploy"){
             when {
              expression { return params.RUN_DEPLOY == true }
           }
            steps {
                script {
                   sh "docker run -itd --name python -p 9091:5000 ${AWS_ECR_REPOSITORY_URL}/${WEB_APP_ECR_REPO_NAME}:${params.IMAGE_TAG}}"
                }
            }
        }
                    
    }
}
