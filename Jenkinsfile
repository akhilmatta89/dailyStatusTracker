pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup & Lint') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    # Lint code
                    flake8 .
                    black --check .
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest -q --junitxml=tests/junit-report.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'tests/junit-report.xml'
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo "Deploying branch ${env.BRANCH_NAME}"
                // Add your deployment steps here
            }
        }
    }

    post {
        success {
            echo "✅ Build successful on branch ${env.BRANCH_NAME}"
        }
        failure {
            echo "❌ Build failed on branch ${env.BRANCH_NAME}"
        }
    }
}
