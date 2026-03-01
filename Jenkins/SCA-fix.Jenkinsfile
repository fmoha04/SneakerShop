    stage('SCA') {
        agent {
          docker {
            image 'owasp/dependency-check:latest'
            args  '--entrypoint="" -u root'
            reuseNode true
          }
        }
        steps {
          withCredentials([string(credentialsId: 'owasp', variable: 'NVD_API_KEY')]) {
            sh """
              mkdir -p reports
              /usr/share/dependency-check/bin/dependency-check.sh \
              --project "SneakerShop" \
              --scan api/web/requirements.txt \
              --format XML \
              --format JSON \
              --out reports \
              --nvdApiKey \$NVD_API_KEY \
              --enableExperimental \
              --disableNodeJS \
              --disableAssembly \
              --disableRubygems \
              --disableCocoapods \
              --disableNugetconf \
              --disableMSBuild \
              --disableComposer \
              --disableMaven
            """
          }
        }
        post {
          always {
            archiveArtifacts artifacts: 'reports/dependency-check-report.json', fingerprint: true
            dependencyCheckPublisher pattern: 'reports/dependency-check-report.xml'
          }
      }
    }
