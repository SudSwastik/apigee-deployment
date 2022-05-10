pipeline {
  agent any
  tools {
    maven 'Maven'
  }
  stages {
    stage('Pre-Build') {
      steps {
        echo 'Pre-Build Stage'
        script {
          kvms = load "kvms.groovy"
        }
      }
    }
    stage('Build') {
      environment {
        // Fetch Common Parameters
        PROFILE = credentials('PROFILE')
        ORG = credentials('ORG')
        APIGEE_USERNAME = credentials('APIGEE_USERNAME')
        APIGEE_PASSWORD = credentials('APIGEE_PASSWORD')
        OPTIONS = credentials('OPTIONS')
        OVERRIDE_DELAY = credentials('OVERRIDE_DELAY')
        DELAY = credentials('DELAY')
      }
      steps {
        echo 'Build Stage'
        script {
          kvms.updateJSON(env.WORKSPACE, env.PROFILE)
        }
        sh 'python3 deploy.py $PROFILE $ORG $APIGEE_USERNAME $APIGEE_PASSWORD \
                $OPTIONS $OVERRIDE_DELAY $DELAY $COMPONENT_JSON'
      }
    }
  }
}