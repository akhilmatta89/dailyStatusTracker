pipeline{
    agent any
    
    tools{
        maven 'maven3.9.11'
    }
    
    triggers {
        githubPush()
    }
    
    options {
        buildDiscarder(logRotator(
            artifactDaysToKeepStr: '4',
            artifactNumToKeepStr: '3',
            daysToKeepStr: '5',
            numToKeepStr: '4'
        ))
        timestamps()
    }
    
    stages{
        stage('CheckoutCode'){
            steps{
                git credentialsId: '81121b4f-64b3-46db-8908-dc33cb0edb99', url: 'https://github.com/akhilmatta89/Petclinic.git'
            }
        }
        stage('BuildPackage'){
            steps{
                sh "mvn clean package"
            }
        }
        
        stage ('Sonar'){
            steps{
                sh "mvn sonar:sonar"
            }
        }
        
        stage ('UploadArtifactsToNexus'){
            steps{
                sh "mvn deploy"
            }
        }
        
        stage ('DeployToTomCat'){
            steps{
               sshagent(['6b398c92-3ef8-4e48-868c-d1626f8cac61']) {
                sh "scp -o StrictHostKeyChecking=no target/petclinic.war ec2-user@13.61.186.132:/opt/apache-tomcat-9.0.109/webapps/"
                }  
            }
        }
    }
post {
        always {
            emailext(
                subject: "Build #${BUILD_NUMBER} - ${JOB_NAME} - ${currentBuild.currentResult}",
                body: """
                <html>
                <body>
                    <h2>Jenkins Build Notification</h2>
                    <p><b>Job:</b> ${JOB_NAME}</p>
                    <p><b>Build Number:</b> ${BUILD_NUMBER}</p>
                    <p><b>Status:</b> ${currentBuild.currentResult}</p>
                    <p><b>Build URL:</b> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                    <br/>
                    <p>Regards,<br/>Akhil Reddy</p>
                </body>
                </html>
                """,
                from: "jenkins@akhil.com",
                to: "akhilreddy2672@gmail.com,likhitha.telukuntla3@gmail.com",
                mimeType: 'text/html'
            )
        }
    }
}
