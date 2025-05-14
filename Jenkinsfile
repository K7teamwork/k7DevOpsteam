pipeline {
    agent any
    stages {
        stage('Setup Python Virtual Environment') {
            steps {
                echo 'Setting Up Venv...'
                sh '''
                chmod +x envsetup.sh
                ./envsetup.sh
                '''
            }
        }
        
        
        stage('Setup Gunicorn Server') {
            steps {
                echo 'Starting Up Gunicorn...'
                sh '''
                chmod +x gunicorn.sh
                ./gunicorn.sh
                '''
            }
        }

        stage('Setup Nginx Server') {
            steps {
                echo 'Starting Up Nginx...'
                sh '''
                chmod +x nginx.sh
                ./nginx.sh
                '''
            }
        }
        
    }
    
}