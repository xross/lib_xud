// This file relates to internal XMOS infrastructure and should be ignored by external users

@Library('xmos_jenkins_shared_library@v0.39.0') _

def clone_test_deps() {
  dir("${WORKSPACE}") {
    sh "git clone git@github.com:xmos/test_support"
    sh "git -C test_support checkout c820ebe67bea0596dabcdaf71a590c671385ac35"
  }
}

getApproval()

pipeline {
  agent {
    label 'x86_64 && linux'
  }
  options {
    buildDiscarder(xmosDiscardBuildSettings())
    skipDefaultCheckout()
    timestamps()
  }
  parameters {
    choice(name: 'TEST_LEVEL', choices: ['smoke', 'default', 'extended'],
            description: 'The level of test coverage to run'
    )
    string(
      name: 'TOOLS_VERSION',
      defaultValue: '-j -b markp_xsim_expose_signals_from_usb_shim latest',
      description: 'The XTC tools version'
    )
    string(
      name: 'XMOSDOC_VERSION',
      defaultValue: 'v7.0.0',
      description: 'The xmosdoc version'
    )
    string(
      name: 'INFR_APPS_VERSION',
      defaultValue: 'v2.1.0',
      description: 'The infr_apps version'
    )
  }

  stages {
    stage('Build examples') {
      steps {
        println "Stage running on ${env.NODE_NAME}"

        script {
            def (server, user, repo) = extractFromScmUrl()
            env.REPO = repo
        }

        dir("${REPO}") {
          checkoutScmShallow()

          dir("examples") {
            withTools(params.TOOLS_VERSION) {
              sh 'cmake -G "Unix Makefiles" -B build'
              sh 'xmake -C build -j'
            }
          }
        }
      }
    }  // Build examples

    stage('Library checks') {
        steps {
            warnError("Library checks failed")
            {
                runLibraryChecks("${WORKSPACE}/${REPO}", "${params.INFR_APPS_VERSION}")
            }
        }
    }

    stage('Documentation') {
      steps {
        dir(REPO) {
          buildDocs()
        }
      }
    }

    stage('Tests')
    {
      steps {
          clone_test_deps()

          withTools(params.TOOLS_VERSION) {
            dir("${REPO}/tests") {
              createVenv(reqFile: "requirements.txt")
              withVenv{
                runPytest("--numprocesses=8 --testlevel=${params.TEST_LEVEL} --enabletracing")
              }
            } // dir
          } // withTools
      } // steps
      post
      {
        failure
        {
          archiveArtifacts artifacts: "${REPO}/tests/logs/*.txt", fingerprint: true, allowEmptyArchive: true
        }
      }
    }

    stage("Archive lib") {
        steps
        {
            archiveSandbox(REPO)
        }
    }
  }
  post {
    cleanup {
      xcoreCleanSandbox()
    }
  }
}
