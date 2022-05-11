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
    stage('healthcheck changes folder'){
        steps {
            script {
                sh '''
                    set +x
                    git diff --name-only HEAD~1..HEAD sharedflows/ > changefile.txt
                    git diff --name-only HEAD~1..HEAD proxies/ >> changefile.txt
                    git diff --name-only HEAD~1..HEAD config/ >> changefile.txt
                    cat changefile.txt
                 '''
              sh 'echo cat changefile.txt'
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





// 

// def call(Map pipelineParams)
// {
// def AGENT_NAME = "docker-builder"
// if (env.BRANCH_NAME == "master") {
//   AGENT_NAME = "docker-builder-prod"
// }
// pipeline {
//    agent {
//     label AGENT_NAME
//   }
//   tools {
//     maven 'Maven'
//     nodejs 'NodeJS'
//   }
//   stages {
//     stage('Pre-Build') {
//       steps {
//         script {
//           echo "${GIT_BRANCH}"
// 	        kvms = load "kvms.groovy"
//           sh 'npm install -g newman'
//           sh 'npm install -g newman-reporter-htmlextra'
//       }
//     }
//     }	
//     stage('healthcheck changes folder')
//      {
//         steps {
//             script {
//                 sh '''
//                     set +x
//                     git diff --name-only HEAD~1..HEAD sharedflows/ > changefile.txt
//                     git diff --name-only HEAD~1..HEAD proxies/ >> changefile.txt
//                     git diff --name-only HEAD~1..HEAD config/ >> changefile.txt
//                     cat changefile.txt
//                  '''
//             }
//     }
//   }
//     stage('health check Status')
//     {
//       steps {
//         script {
//          sh 'python3 -m pip install asyncio aiohttp --user'
//          sh 'python3 health-check.py dev changefile.txt'
//       }
//     }
//     }
//     stage('Deploy') {
//         environment {
//         // Fetch Common Parameters
//         PROFILE = "${PROFILE}"
//         HOST = credentials('HOST')
//         ORG = credentials('ORG')
//         APIGEE_USERNAME = credentials('APIGEE_USERNAME')
//         APIGEE_PASSWORD = credentials('APIGEE_PASSWORD')
//         OPTIONS = credentials('OPTIONS')
//         OVERRIDE_DELAY = credentials('OVERRIDE_DELAY')
//         DELAY = credentials('DELAY')
//       }
//       steps {
//         script {
//            kvms.updateJSON(env.WORKSPACE, env.PROFILE)
//         }
//         sh 'python3 deploy.py $PROFILE $HOST $ORG $APIGEE_USERNAME $APIGEE_PASSWORD $OPTIONS $OVERRIDE_DELAY $DELAY'
//          // deploy(PROFILE= env.PROFILE, env.HOST, ORG= env.ORG, APIGEE_USERNAME= env.APIGEE_USERNAME, APIGEE_PASSWORD= env.APIGEE_PASSWORD, OPTIONS= env.OPTIONS, OVERRIDE_DELAY= env.OVERRIDE_DELAY, DELAY= env.DELAY)
//     }
//     }
//   }
// }
// }
