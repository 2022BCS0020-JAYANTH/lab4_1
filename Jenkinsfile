pipeline {
    agent any

    environment {
        DOCKER_REPO = "jayanthbcs20/wine-inference"
        VENV_DIR = "venv"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh """
                python3 -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Train Model') {
            steps {
                sh """
                . ${VENV_DIR}/bin/activate
                python scripts/train.py
                """
            }
        }

        stage('Read Metrics') {
            steps {
                script {
                    def metrics = readJSON file: 'app/artifacts/metrics.json'

                    env.CURRENT_R2 = metrics.r2.toString()
                    env.CURRENT_MSE = metrics.mse.toString()

                    echo "MODEL METRICS"
                    echo "2022BCS0020 - Jayanth"
                    echo "R2  : ${env.CURRENT_R2}"
                    echo "MSE : ${env.CURRENT_MSE}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REPO}:${BUILD_NUMBER}")
                }
            }
        }

        stage('Run Container & Test (curl)') {
            steps {
                sh """
                    
                    docker rm -f wine-test || true
                    
                    docker run -d -p 5000:5000 --name wine-test ${DOCKER_REPO}:${BUILD_NUMBER}
                    
                    sleep 10
                    
                    curl http://localhost:5000/
                    
                    docker stop wine-test
                    docker rm wine-test
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {

                        sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker tag ${DOCKER_REPO}:${BUILD_NUMBER} ${DOCKER_REPO}:latest
                        docker push ${DOCKER_REPO}:${BUILD_NUMBER}
                        docker push ${DOCKER_REPO}:latest
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', fingerprint: true
        }
        success {
            echo "Pipeline completed successfully"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}
