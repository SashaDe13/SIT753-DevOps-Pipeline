pipeline {
  agent any
  tools {
        sonarQube 'SonarQube Scanner'
  }
  environment {
    PATH = "/Users/sashane/.docker/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    APP_NAME = 'sit753-task-api'
    STAGING_CONTAINER = 'sit753-task-api-staging'
    PROD_CONTAINER = 'sit753-task-api-prod'
    STAGING_PORT = '5001'
    PROD_PORT = '5002'
  }
  options { timestamps(); disableConcurrentBuilds() }
  stages {
    stage('Build') {
      steps {
        sh '''
          python3 -m venv venv
          . venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          docker build -t ${APP_NAME}:${BUILD_NUMBER} .
          docker save ${APP_NAME}:${BUILD_NUMBER} | gzip > ${APP_NAME}-${BUILD_NUMBER}.tar.gz
        '''
        archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
      }
    }
    stage('Test') {
      steps {
        sh '''
          . venv/bin/activate
          PYTHONPATH=. pytest -v --cov=app --cov-report=term --cov-report=xml
        '''
      }
      post { always { archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true } }
    }
    stage('Code Quality') {
      steps {
        withSonarQubeEnv('SonarQube') { sh 'sonar-scanner' }
      }
    }
    stage('Security') {
      steps {
        sh '''
          . venv/bin/activate
          bandit -r app.py -f json -o bandit-report.json
          docker run --rm aquasec/trivy:latest image --severity HIGH,CRITICAL ${APP_NAME}:${BUILD_NUMBER}
        '''
      }
      post { always { archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true } }
    }
    stage('Deploy') {
      steps {
        sh '''
          docker rm -f ${STAGING_CONTAINER} 2>/dev/null || true
          docker run -d --name ${STAGING_CONTAINER} -p ${STAGING_PORT}:5000 ${APP_NAME}:${BUILD_NUMBER}
          sleep 3
          curl --fail http://localhost:${STAGING_PORT}/health
        '''
      }
    }
    stage('Release') {
      steps {
        sh '''
          docker tag ${APP_NAME}:${BUILD_NUMBER} ${APP_NAME}:v1.0.${BUILD_NUMBER}
          docker rm -f ${PROD_CONTAINER} 2>/dev/null || true
          docker run -d --name ${PROD_CONTAINER} -p ${PROD_PORT}:5000 --restart unless-stopped ${APP_NAME}:v1.0.${BUILD_NUMBER}
          sleep 3
          curl --fail http://localhost:${PROD_PORT}/health
        '''
      }
    }
    stage('Monitoring') {
      steps {
        sh '''
          curl --fail http://localhost:${PROD_PORT}/health
          docker inspect --format='{{json .State.Health}}' ${PROD_CONTAINER}
        '''
      }
    }
  }
  post {
    success { echo "Pipeline completed successfully for build ${BUILD_NUMBER}" }
    failure { echo "Pipeline failed; inspect the failed stage before release." }
  }
}
