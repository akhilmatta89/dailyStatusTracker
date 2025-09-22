// pipeline {
//     agent any

//     stages {
//         stage('Checkout') {
//             steps {
//                 checkout scm
//             }
//         }

//         stage('Setup & Lint') {
//             steps {
//                 sh '''
//                     python3 -m venv venv
//                     . venv/bin/activate
//                     pip install --upgrade pip
//                     pip install -r requirements.txt
//                     flake8 . || true
//                 '''
//             }
//         }

//         stage('Unit Tests') {
//             steps {
//                 sh '''
//                     . venv/bin/activate
//                     pytest -q --junitxml=tests/junit-report.xml
//                 '''
//             }
//             post {
//                 always {
//                     junit allowEmptyResults: true, testResults: 'tests/junit-report.xml'
//                 }
//             }
//         }

//         stage('Deploy') {
//             when {
//                 branch 'main'
//             }
//             steps {
//                 echo "Deploying branch ${env.BRANCH_NAME}"
//                 // Add your deployment steps here
//             }
//         }
//     }

//     post {
//         success {
//             echo "✅ Build successful on branch ${env.BRANCH_NAME}"
//         }
//         failure {
//             echo "❌ Build failed on branch ${env.BRANCH_NAME}"
//         }
//     }
// }
pipeline {
    agent {
        label 'node-1'
    }
    environment {
        SSH_CREDENTIALS = 'deploy-ssh-key'       // Jenkins SSH key credential
        DEPLOY_HOST = 'ubuntu@deploy-host'       // Replace with your host
        VENV_PATH = "${env.WORKSPACE}/venv"
    }
    options {
        skipDefaultCheckout(false)
        timestamps()
    }
    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup & Lint') {
            steps {
                sh '''
                    # Create virtual environment if not exists
                    if [ ! -d "${VENV_PATH}" ]; then
                        python3 -m venv ${VENV_PATH}
                    fi

                    # Activate virtualenv
                    . ${VENV_PATH}/bin/activate

                    # Upgrade pip and install requirements
                    pip install --upgrade pip
                    pip install -r requirements.txt

                    # Run flake8 lint (will not fail pipeline)
                    flake8 . || true
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate

                    # Run all test cases in repo and generate JUnit XML report
                    pytest --junitxml=tests/junit-report.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'tests/junit-report.xml'
                }
            }
        }

        stage('Deploy') {
            steps {
                sshagent(credentials: [env.SSH_CREDENTIALS]) {
                    sh """
                        # Example: copy docker-compose deploy file and bring up services
                        scp docker-compose.deploy.yml ${DEPLOY_HOST}:/home/ubuntu/docker-compose.yml
                        ssh ${DEPLOY_HOST} 'docker-compose -f /home/ubuntu/docker-compose.yml up -d --no-deps --build'
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build, tests & deploy successful"
        }
        unstable {
            echo "⚠️ Build successful but some tests or lint issues exist"
        }
        failure {
            echo "❌ Build failed"
        }
    }
}
