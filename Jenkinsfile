pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python Env') {
      steps {
        // Using a virtual environment is optional but good practice
        sh '''
          python --version
          python -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Lint') {
      steps {
        sh '''
          . venv/bin/activate
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
        // Add your deployment steps here, e.g. SSH to server, SCP files, run scripts etc.
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
